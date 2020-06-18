from django.shortcuts import render, redirect
from django.http import JsonResponse
from crispy_forms.helper import FormHelper
from django import forms
from django.forms import (Form, ImageField, CharField)
from django.core.files.base import ContentFile
from django.contrib.auth.models import Group
from webpush import send_user_notification
from problem.models import Person
from .models import Appeal, Image, Result
from mcur.settings import MEDIA_ROOT, MEDIA_URL, WEBPUSH_SETTINGS

import zipfile


class AppealForm(Form):
    nomdobr = CharField(label=u'Номер обращения')
    text = CharField(label=u'Комментарий', widget=forms.Textarea, required=False)
    image = ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)

    class Meta:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.widgets['text'].template_name = "widgets/textarea.html"


def del_message(request):
    if request.user.has_perm('problem.user_moderator') or request.user.has_perm('block.moderator'):
        if request.method == 'POST':
            content = {}
            result = Result.objects.get(pk=int(request.POST['pk']))
            app = result.block
            result.delete()
            if Result.objects.filter(block=app).exists():
                a = Result.objects.filter(block=app).order_by('-datecre')
                stat = a[0].chstatus
                app.status = stat
            else:
                app.status = '0'
            app.save()
            return JsonResponse(content)


def view_message(request):
    if request.user.has_perm('problem.user_moderator') or request.user.has_perm('block.moderator'):
        if request.method == 'POST':
            content = {}
            app = Appeal.objects.get(nomdobr=request.POST['pk'])
            result = Result.objects.filter(block=app)
            content['message'] = []
            for i in result:
                content['message'].append({'text': i.text, 'status': i.get_chstatus_display(), 'pk': i.pk,
                                           'user': f'{i.user.first_name} {i.user.last_name}',
                                           'datecre': i.datecre.strftime('%d.%m.%Y'), 'nomkom': i.nomkom})
            return JsonResponse(content)


def addresult(request):
    if request.user.has_perm('problem.user_moderator') or request.user.has_perm('block.moderator') or request.user.has_perm('block.executor'):
        if request.method == 'POST':
            di = request.POST
            blo = Appeal.objects.get(nomdobr=di['pk'])
            res = Result.objects.create(block=blo, chstatus=di['status'], text=di['text'], nomkom=di['nomkom'],
                                        user=request.user)
            res.save()
            blo.status = di['status']
            print(1)
            if blo.status == '0':
                group = Group.objects.get(pk=6)
                users = Person.objects.filter(groups=group)
                blo.text = di['text']
                for i in users:
                    payload = {"head": "Изменен статус", "body": f"Обращение №{blo.nomdobr}. Изменен статус на: {blo.get_status_display()}"}
                    send_user_notification(user=i, payload=payload, ttl=1000)
            else:
                payload = {"head": "Изменен статус", "body": f"Обращение №{blo.nomdobr}. Изменен статус на: {blo.get_status_display()}"}
                send_user_notification(user=blo.user, payload=payload, ttl=1000)
            blo.save()
            print(f'Обращение: {blo.nomdobr}, новый статус: {blo.get_status_display()}')
            content = {}
            return JsonResponse(content)


def QStolist(queryset):
    temp = []
    for j in queryset:
        temp.append({'pk': j.pk, 'nomd': j.nomdobr, 'datecre': j.datecre.strftime('%d.%m.%Y'), 'text': j.text,
                      'status': j.get_status_display(), 'user': f'{j.user.first_name} {j.user.last_name}'})
    return temp


def table(request):
    if request.user.has_perm('problem.user_moderator') or request.user.has_perm('block.executor'):
        if request.method == 'POST':
            di = request.POST
            status = di['status'].split('-')[1]
            appe = Appeal.objects.filter(status=status)
            tables = QStolist(appe)
            cont = {'appe': tables}
            return JsonResponse(cont)


def obr_view(request):
    if request.method == 'POST':
        if Appeal.objects.filter(nomdobr=request.POST['pk']).exists():
            app = Appeal.objects.get(nomdobr=request.POST['pk'])
            image = False
            message = False
            if Image.objects.filter(otv=app).exists():
                image = True
            if Result.objects.filter(block=app).exists():
                message = True
            temp = {'pk': app.pk, 'nomd': app.nomdobr, 'datecre': app.datecre.strftime('%d.%m.%Y'),'status': app.get_status_display(),
                    'user': f'{app.user.first_name} {app.user.last_name}', 'text': app.text,
                    'datebzm': app.datebzm.strftime('%d.%m.%Y'), 'image': image, 'message': message}
            content = {'app': temp}
            return JsonResponse(content)


def downimage(request):
    if request.user.has_perm('problem.user_moderator') or request.user.has_perm('block.executor'):
        if request.method == 'POST':
            a = Appeal.objects.get(nomdobr=request.POST['pk'])
            if Image.objects.filter(otv=a).exists():
                allfileqs = Image.objects.filter(otv=a)
                if len(allfileqs) > 1:
                    name = f'zip/{a.nomdobr}.zip'
                    with zipfile.ZipFile(MEDIA_ROOT + name, 'w') as myzip:
                        for i in allfileqs:
                            t = f'{MEDIA_ROOT}{i.file}'
                            myzip.write(t, arcname=i.file.name)
                    content = {'url': MEDIA_URL + name}
                    return JsonResponse(content)
                else:
                    content = {'url': allfileqs[0].file.url}
                    return JsonResponse(content)
            else:
                return redirect('blockindex')


def main(request):
    if request.user.has_perm('problem.user_moderator') or request.user.has_perm('block.executor'):
        if request.method == 'POST':
            form = AppealForm(request.POST, request.FILES)
            if form.is_valid():
                if not Appeal.objects.filter(nomdobr=form.cleaned_data['nomdobr']).exists():
                    appe = Appeal.objects.create(nomdobr=form.cleaned_data['nomdobr'], text=form.cleaned_data['text'],
                                                 user=request.user)
                    for f in request.FILES.getlist('image'):
                        data = f.read()
                        photo = Image(otv=appe)
                        photo.file.save(f.name, ContentFile(data))
                        photo.save()
                    appe.save()
                    group = Group.objects.get(pk=6)
                    users = Person.objects.filter(groups=group)
                    for i in users:
                        payload = {"head": "На блокировку", "body": f"Обращение №{appe.nomdobr}"}
                        send_user_notification(user=i, payload=payload, ttl=1000)
            return redirect('blockindex')
        else:
            addform = AppealForm
            content = {}
            a = Appeal.objects.filter(status='0')
            table = QStolist(a)
            notkey = WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY']
            content['table'] = table
            content['addform'] = addform
            content['NOTIFICATION_KEY'] = notkey
            return render(request, 'problem/block.html', content)
