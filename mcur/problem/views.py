# Django
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.core.files.base import ContentFile

# django_tables2
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableMixin
from django_tables2.paginators import LazyPaginator
from django_tables2.export.views import ExportMixin, TableExport

# django_filters
from django_filters.views import FilterView

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.settings import api_settings

#reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.units import mm

#project
from .models import (Problem, Curator, Term, Answer, Image, Status, Termhistory, Department, Person, Category,
                     UserProfile, Minis, Author)
from parsers.models import ActionHistory, Action, Parser
from .tables import ProblemTable, ParsTable, UserTable, HistTable
from .forms import (PrAdd, TermForm, AnswerForm,ResolutionForm, CreateUser, TyForm)
from .filter import ProblemListView, ProblemFilter
from .logick import lk_dispatcher, lk_executor, lk_moderator, lk_ty, prob_func
from mcur import settings
from .api import api_func

# other
from datetime import date, timedelta, datetime
from sys import platform
from operator import itemgetter
import xlwt
import random
import os
import logging
import traceback


logger = logging.getLogger('django.server')
logger_mail = logging.getLogger('django.request')
logger_error = logging.getLogger('file_error')
chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('__all__')


@api_view(['POST'])
def dopaction(request):
    pkstat = settings.NO_VISIBLE
    allkolvo = 0
    prob = Problem.objects.filter(Q(visible='1') & (Q(status__pk__in=pkstat[0])))
    allkolvo += len(prob)
    prob = Problem.objects.filter(Q(visible='1') & (Q(status__pk__in=pkstat[1])))
    allkolvo += len(prob)
    return JsonResponse({'kolvo': allkolvo})


@api_view(['POST'])
def apis(request):
    zapr = request.POST
    if 'token' in zapr :
        token = zapr['token']
        if User.objects.filter(userprofile__uuid=token).exists():
            if 'action' in zapr:
                act = zapr['action']
                user = User.objects.get(userprofile__uuid=token)
                text = {'username': user.username, 'action': act}
                return JsonResponse({'status': 'successfully', 'text': text})
            else:
                return JsonResponse({'status': 'error', 'text': 'Inaccessible action'})
        else:
            return JsonResponse({'status': 'error', 'text': 'Invalid Token'})
    else:
        return JsonResponse({'status': 'error', 'text': 'Invalid request', 'request': zapr})

@api_view(['GET'])
def api_problem(request):
    if request.method == 'GET':
        prob = Problem.objects.filter(visible='1')
        serializer = ProblemSerializer(prob, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_problem_detail(request, np):
    if request.method == 'GET':
        prob = Problem.objects.get(nomdobr=np)
        serializer = ProblemSerializer(prob)
        return Response(serializer.data)


class ActionSerializer(serializers.Serializer):
    title = serializers.CharField()
    nom = serializers.IntegerField()
    message = serializers.CharField()


class ProblemsSerializer(serializers.Serializer):
    nomdobr = serializers.CharField()
    dateotv = serializers.DateField(format='%d.%m.%Y')
    temat = serializers.CharField()
    podcat = serializers.CharField()
    statussys = serializers.CharField(source='get_statussys_display')
    status = serializers.CharField()

    class Meta:
        model = Problem


class ActionObject(object):
    def __init__(self, title, nom, message):
        self.title = title
        self.nom = nom
        self.message = message


@api_view(['POST'])
def api_action(request):
    if request.user.has_perm('problem.user_moderator'):
        if request.method == 'POST':
            nowdatetime = datetime.now()
            nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
            if request.POST['action'] == 'action1':
                title = 'Скрытие обращений'
                status = settings.NO_VISIBLE[0]
                status2 = settings.NO_VISIBLE[1]
                allprob = 0
                prob = Problem.objects.filter(Q(visible='1') & (Q(status__pk__in=status)))
                allprob += len(prob)
                prob.update(visible='0')
                prob = Problem.objects.filter(Q(visible='1') & (Q(status__pk__in=status2)))
                allprob += len(prob)
                prob.update(visible='2')
                mes = f'''Успешно выполнено!
    Количество исправленных обращения: {allprob}'''
                nom = 0
            elif request.POST['action'] == 'action2':
                a = ActionHistory()
                a.act = Action.objects.get(nact='2')
                a.arg = 'all'
                a.save()
                title = 'Добавление задачи'
                mes = f'''Успешно выполнено!
                Задание запущено.'''
                nom = 0
            elif request.POST['action'] == 'action3':
                a = ActionHistory()
                a.act = Action.objects.get(nact='8')
                a.save()
                title = 'Добавление задачи'
                mes = f'''Успешно выполнено!
                Задание запущено.'''
                nom = 0
            elif request.POST['action'] == 'action4':
                data = (nowdate - timedelta(3)).strftime('%d.%m.%Y')
                tempdate = nowdate.strftime('%d.%m.%Y')
                a = ActionHistory()
                a.act = Action.objects.get(nact='5')
                a.arg = f'{data},{tempdate}'
                a.save()
                title = 'Добавление задачи'
                mes = f'''Успешно выполнено!
                Задание запущено.'''
                nom = 0
            elif request.POST['action'] == 'action5':
                a = ActionHistory()
                a.act = Action.objects.get(nact='7')
                a.save()
                title = 'Добавление задачи'
                mes = f'''Успешно выполнено!
                Задание запущено.'''
                nom = 0
            elif request.POST['action'] == 'action6':
                data = (nowdate - timedelta(3)).strftime('%d.%m.%Y')
                a = ActionHistory()
                a.act = Action.objects.get(nact='6')
                a.arg = data
                a.save()
                title = 'Добавление задачи'
                mes = f'''Успешно выполнено!
                Задание запущено.'''
                nom = 0
            elif request.POST['action'] == 'action7':
                a = ActionHistory()
                a.act = Action.objects.get(nact='9')
                a.save()
                title = 'Добавление задачи'
                mes = f'''Успешно выполнено!
                Задание запущено.'''
                nom = 0
            elif request.POST['action'] == 'action8':
                a = ActionHistory()
                a.act = Action.objects.get(nact='10')
                a.save()
                title = 'Добавление задачи'
                mes = f'''Успешно выполнено!
                Задание запущено.'''
                nom = 0
            else:
                title = 'Ошибка'
                mes = 'Ошибка при выполнении!'
                nom = 1
            a = ActionObject(title=title, nom=nom, message=mes)
            serializer = ActionSerializer(a)
            return JsonResponse(serializer.data, safe=False)
    else:
        title = 'Ошибка'
        mes = 'Нет прав на выполнение данной операции!'
        nom = 1
        a = ActionObject(title=title, nom=nom, message=mes)
        serializer = ActionSerializer(a)
        return JsonResponse(serializer.data, safe=False)


class AnswerSerializer(serializers.Serializer):
    kolvosogl = serializers.IntegerField()
    kollno = serializers.IntegerField()


class AnswerObject(object):
    def __init__(self, kollno, kolvosogl):
        self.kollno = kollno
        self.kolvosogl = kolvosogl


@csrf_exempt
def api_answer_detail(request):
    if request.method == 'POST':
        answ = Answer.objects.filter(status='0')
        prob = len(Problem.objects.filter(visible='1', statussys='2'))
        a = AnswerObject(kollno=prob, kolvosogl=len(answ))
        serializer = AnswerSerializer(a)#, many=True)
        return JsonResponse(serializer.data, safe=False)


def Mailsend(email, date, nomd):
    data = f'''
<p>Вам направлена задача сроком до {date}. На обращение <a href='https://skiog.ru/problem/{nomd}'>№{nomd}</a></p>
<p></p>
<p>______________<p>
<p>Администрация информационной системы skiog.ru </p>
'''
    emai = email
    send_mail('SKIOG', None, 'noreply@skiog.ru', [emai], fail_silently=False, html_message=data)


class error_page:
    def e400(request, exception):
        errors = 'Ошибка 400!'
        num = 400
        head = 'Упс! Ошибка сервера!'
        cont = 'Просьба обратиться к администратору системы!'
        status = 'danger'
        content = {"error": errors, 'num': num, 'head': head, 'cont': cont, 'status': status}
        return render(request, 'problem/errorpage.html', {'content': content})

    def e404(request, exception):
        errors = 'Ошибка 404!'
        num = 404
        head = 'Упс! Страница не найдена!'
        cont = 'Данной страницы не существует!'
        status = 'warning'
        content = {"error": errors, 'num': num, 'head': head, 'cont': cont, 'status': status}
        return render(request, 'problem/errorpage.html', {'content': content})

    def e500(request):
        errors = 'Ошибка 500!'
        num = 500
        head = 'Упс! Ошибка сервера!'
        cont = 'Просьба обратиться к администратору системы!'
        status = 'danger'
        content = {"error": errors, 'num': num, 'head': head, 'cont': cont, 'status': status}
        return render(request, 'problem/errorpage.html', {'content': content})


def proverka(request, term):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if not request.user.has_perm(term):
            return redirect('index')


def Answer_approve(request, pk):
    term = 'problem.user_moderator'
    proverka(request, term)
    anw = Answer.objects.get(pk=pk)
    anw.status = '1'
    anw.term.status = '2'
    anw.term.anwr = True
    anw.save()
    anw.term.save()
    z = anw.term.problem.nomdobr
    return redirect('problem',pk=z)


def Answer_modify(request, pk):
    term = 'problem.user_moderator'
    proverka(request, term)
    anw = Answer.objects.get(pk=pk)
    anw.term.status = '0'
    anw.term.anwr = False
    anw.term.save()
    z = anw.term.problem.nomdobr
    anw.delete()
    return redirect('problem',pk=z)


def prob(request, pk):
    back = str(request.META.get('HTTP_REFERER'))
    if back.find('None') != -1:
        back = False
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            api = api_func('problem')()
            api(request=request)
            return JsonResponse(api.context)
        else:
            if Problem.objects.filter(nomdobr=pk).exists():
                c = False
                terms = []
                prob = Problem.objects.get(nomdobr=pk)
                if request.user.has_perm('problem.user_moderator'):
                    c = True
                    terms = prob.terms.all()
                nowdatetime = datetime.now()
                nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
                userr = User.objects.get(username=request.user.username)
                tyform = TyForm()
                if userr.userprofile.ty == prob.ciogv and userr.userprofile.ty != None:
                    c = True
                    temp = prob.terms.all()
                    if len(temp) > 0:
                        for i in temp:
                            terms.append(i)
                else:
                    if not c:
                        temp = prob.terms.filter(Q(org=userr.userprofile.org) | Q(curat=userr.userprofile.dep) | Q(curatuser=userr))
                        if len(temp) > 0:
                            for i in temp:
                                terms.append(i)
                        resol = Termhistory.objects.filter(Q(curat=userr.userprofile.dep) | Q(curatuser=userr))
                        if len(resol) > 0:
                            for i in resol:
                                if not i.term in terms:
                                    terms.append(i.term)
                if c or len(terms) > 0:
                    termadd = TermForm()
                    answeradd = AnswerForm()
                    if userr.has_perm('problem.user_moderator'):
                        dep = Department.objects.all()
                        userorg = Person.objects.all()
                    elif userr.has_perm('problem.user_dispatcher'):
                        dep = Department.objects.filter(org=userr.userprofile.org)
                        userorg = Person.objects.filter(userprofile__org=userr.userprofile.org)
                    elif userr.has_perm('problem.user_executor'):
                        if userr.userprofile.dep != None:
                            dep = Department.objects.filter(name=userr.userprofile.dep.name)
                            userorg = Person.objects.filter(userprofile__dep__in=dep)
                        else:
                            dep = []
                            userorg = Person.objects.filter(userprofile__org=userr.userprofile.org)
                    elif userr.has_perm('problem.user_ty'):
                        dep = None
                        userorg = None
                    resform = ResolutionForm(curat_qs=dep, curatuser_qs=userorg)
                    return render(request, 'problem/problem.html', {'tyform': tyform, 'answeradd': answeradd,
                                                                    'formadd': termadd, 'np': prob, 'terms': terms,
                                                                    'resform': resform, 'back': back})
                else:
                    messages.error(request, 'Нет доступа к обращению.')
                    return redirect('index')
            else:
                return redirect('index')


def zaptable(request):
    for i in range(0,51):
        temp = random.randint(3000000,4000000)
        a = Problem()
        a.nomdobr = temp
        a.save()
    return redirect('index')


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('index')


def add(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.has_perm('problem.add_Problem'):
            if not Problem.objects.filter(nomdobr=request.POST['nomdobr']).exists():
                if request.method == 'POST':
                    formadd = PrAdd(request.POST)
                    if formadd.is_valid():
                        formadd.save()
                        return redirect("problem", pk= Problem.objects.get(nomdobr=request.POST['nomdobr']).pk)
                    else:
                        return redirect("index")
                else:
                    messages.warning(request, 'Данное обращение существует.')
                    return redirect("index")
            else:
                return redirect("problem", pk=Problem.objects.get(nomdobr=request.POST['nomdobr']).pk)


def lk(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            if request.user.has_perm('problem.user_moderator'):
                a = prob_func('moderator')()
            elif request.user.has_perm('problem.user_dispatcher'):
                a = prob_func('dispatcher')()
            elif request.user.has_perm('problem.user_executor'):
                a = prob_func('executor')()
            elif request.user.has_perm('problem.user_ty'):
                a = prob_func('ty')()
            a(request=request)
            return JsonResponse({'boxn': a.box, 'kolvo': len(a.prob), 'mes': 'succes'})
        else:
            return render(request, 'problem/lk.html')


opic = {
    'closed': 'Закрытые обращения',
    'noproblem': 'Не распределенные обращения',
    'allproblem': 'Все обращения',
    'meproblem': 'Мои обращения',
    'podxproblem': 'Подходит срок обращения',
    'todayproblem': 'Обращения на сегодня',
    'prosrproblem': 'Просроченные обращения',
    'typroblem': 'Обращения без ТУ',
    'fuproblem': 'Обещанные обращения'
}


def problems(request, action):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        context = dict()
        userlk = User.objects.get(username=request.user.username)
        if userlk.has_perm('problem.user_moderator'):
            a = prob_func('moderator')()
        elif userlk.has_perm('problem.user_dispatcher'):
            a = prob_func('dispatcher')()
        elif userlk.has_perm('problem.user_executor'):
            a = prob_func('executor')()
        elif userlk.has_perm('problem.user_ty'):
            a = prob_func('ty')()
        a(request=request, action=action)
        prob = a.prob
        filterall = ProblemFilter(request.GET, queryset=prob)
        table = ProblemTable(filterall.qs)
        export_format = request.GET.get("_export", None)
        try:
            if TableExport.is_valid_format(export_format):
                exporter = TableExport(export_format, table)
                return exporter.response(f"table-{action}.{export_format}")
        except:
            logger_error.error(traceback.format_exc())
        RequestConfig(request, ).configure(table)
        context['filter'] = filterall
        context['table'] = table
        context['name'] = opic[action]
        context['dop'] = f'Всего: {len(filterall.qs)}.'
        context['title'] = opic[action]
        return render(request, "problem/allproblem.html", context)


def search(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            nd = request.POST['pk']
            if Problem.objects.filter(nomdobr=nd).exists():
                prob = Problem.objects.get(nomdobr=nd)
                return redirect("problem", pk=prob.nomdobr)
            else:
                return redirect('index')
        return redirect('index')


def addanswer(request, pk):
    term = Term.objects.get(pk=pk)
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            formadd = AnswerForm(request.POST, request.FILES)
            if formadd.is_valid():
                answr = Answer.objects.create(text=formadd.cleaned_data['text'], user=request.user)
                for f in request.FILES.getlist('image'):
                    data = f.read()
                    photo = Image(otv=answr)
                    photo.file.save(f.name, ContentFile(data))
                    photo.save()
                answr.term = term
                answr.save()
                term.status = '1'
                term.anwr = True
                term.save()
                return redirect("problem", pk=term.problem.nomdobr)
            else:
                return redirect('index')
        else:
            return redirect('index')


def development(request):
    return render(request, 'problem/development.html')


def resolutionadd(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        term = Term.objects.get(pk=pk)
        if request.method == 'POST':
            resform = ResolutionForm(request.POST, curat_qs=None, curatuser_qs=None)
            if resform.is_valid():
                a = resform.save()
                a.term = term
                a.user = request.user
                if a.curatuser:
                    temp = f'{a.date.day}.{a.date.month}.{a.date.year}'
                    #Mailsend(a.curatuser.email, temp, a.term.problem.nomdobr)
                a.save()
                return redirect("problem", pk=term.problem.nomdobr)
            else:
                redirect("problem", pk=term.problem.nomdobr)


def createuser(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = 'Создание пользователя'
        if request.user.has_perm('problem.user_supermoderator'):
            if request.method == 'POST':
                password = ''
                for i in range(8):
                    password += random.choice(chars)
                user = User.objects.create_user(request.POST['username'], request.POST['email'], password)
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                org = Curator.objects.get(pk=request.POST['org'])
                a = UserProfile(user=user, org=org)
                if request.POST['dep']:
                    dep = Department.objects.get(pk=request.POST['dep'])
                    a.dep = dep
                a.save()
                group = Group.objects.get(pk=request.POST['group'])
                user.groups.add(group)
                user.save()
                mes = f'''Пользователь создан.\n
Логин: {request.POST['username']}\n
Пароль: {password}'''
                nom = 0
                a = ActionObject(title=title, nom=nom, message=mes)
                serializer = ActionSerializer(a)
                return JsonResponse(serializer.data, safe=False)
            else:
                mes = 'Ошибка, неправильный запрос.'
                nom = 1
                a = ActionObject(title=title, nom=nom, message=mes)
                serializer = ActionSerializer(a)
                return JsonResponse(serializer.data, safe=False)
        else:
            mes = 'Ошибка, недостаточно прав.'
            nom = 1
            a = ActionObject(title=title, nom=nom, message=mes)
            serializer = ActionSerializer(a)
            return JsonResponse(serializer.data, safe=False)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.has_perm('problem.user_moderator'):
            if request.method == 'POST':
                api = api_func('dashboard')()
                api(request=request)
                return JsonResponse(api.context)
            else:
                return render(request, 'problem/dashboard.html')


def export_pdf(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        # Create the HttpResponse object with the appropriate PDF headers.
        prob = Problem.objects.get(nomdobr=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="d-{prob.nomdobr}.pdf"'
        # Create the PDF object, using the response object as its "file."
        times = os.path.join(settings.BASE_DIR, 'font', 'times.ttf')
        style = getSampleStyleSheet()
        width, height = A4
        row = 800
        c = canvas.Canvas(response, pagesize=A4)
        pdfmetrics.registerFont(TTFont("Times", times))
        url = 'http://skiog.ru/problem/'
        barcode_string = f'<font name="Times" size="16">Обращение №<a href="{url}{prob.nomdobr}" underline="True">{prob.nomdobr}</a></font>'
        p = Paragraph(barcode_string, style=style["Normal"])
        p.wrapOn(c, width, height)
        p.drawOn(c, 20, row, mm)
        barcode_string = f'<font name="Times" size="16">Категория: </font> <font name="Times" size="14"> {prob.temat}</font>'
        p = Paragraph(barcode_string, style=style["Normal"])
        p.wrapOn(c, width, height)
        p.drawOn(c, 20, row-25, mm)
        barcode_string = f'<font name="Times" size="16">Подкатегория: </font> <font name="Times" size="14"> {prob.podcat}</font>'
        p = Paragraph(barcode_string, style=style["Normal"])
        p.wrapOn(c, width, height)
        p.drawOn(c, 20, row-50, mm)
        barcode_string = f'<font name="Times" size="16">Адрес: </font> <font name="Times" size="14"> {prob.adres}</font>'
        p = Paragraph(barcode_string, style=style["Normal"])
        p.wrapOn(c, width, height)
        p.drawOn(c, 20, row-75, mm)
        barcode_string = f'<font name="Times" size="16">Дата ответа по доброделу: </font> <font name="Times" size="14"> {prob.dateotv.day}.{prob.dateotv.month}.{prob.dateotv.year}</font>'
        p = Paragraph(barcode_string, style=style["Normal"])
        p.wrapOn(c, width, height)
        p.drawOn(c, 20, row-100, mm)
        barcode_string = f'''<font name="Times" size="16">Текс обращения:
    </font> <font name="Times" size="14">
    <p>{prob.text}</p>
    </font>'''
        p = Paragraph(barcode_string, style=style["Normal"])
        p.wrapOn(c, width-10, height)
        p.drawOn(c, 20, row-250, mm)
        # Close the PDF object cleanly, and we're done.
        c.setTitle(prob.nomdobr)
        c.showPage()
        c.save()
        return response


def statandact(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.has_perm('problem.user_supermoderator'):
            content = {}
            content['status'] = ['Закрыто', 'Получен ответ', 'Решено', 'На рассмотрении', 'На уточнении', 'Премодерация', 'Премодерация (незавершённая регистрация)']
            content['kolvo'] = []
            for i in content['status']:
                content['kolvo'].append(len(Problem.objects.filter(visible='1', status__name=i)))
            if request.method == 'POST':
                title = 'Действия'
                temp = {}
                temp['title'] = title
                if request.POST['refresh'] == '1':
                    temp['kolvo'] = content['kolvo']
                    temp['message'] = 'График успешно обновлен.'
                    temp['nom'] = 0
                    return JsonResponse(temp)
                else:
                    temp['message'] = 'Ошибка, неправильный запрос.'
                    temp['nom'] = 1
                    return JsonResponse(temp)
            now = datetime.now()
            a = datetime(now.year, now.month, now.day)
            parser = Parser.objects.all()
            table = ParsTable(parser)
            action = ActionHistory.objects.filter(Q(status='0') | Q(lastaction__range=(a, now)))
            table1 = HistTable(action)
            RequestConfig(request, ).configure(table)
            return render(request, 'problem/statandact.html', {'parsers': table, 'action': table1, 'content': content})
        else:
            return redirect('index')


def listuser(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.has_perm('problem.user_supermoderator'):
            users = User.objects.all()
            table = UserTable(users)
            formcreate = CreateUser()
            return render(request, 'problem/listuser.html', {'table': table, 'formcreate': formcreate})
        else:
            return redirect('index')


def zapros(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.has_perm('problem.user_moderator'):
            if request.GET:
                if request.GET['action'] == 'api':
                    if request.GET['org']:
                        temp = request.GET['org']
                        org = Curator.objects.get(pk=temp)
                        dep = Department.objects.filter(org=org)
                        temp = []
                        for i in dep:
                            temp.append([i.pk, i.name])
                        return JsonResponse({'dep': temp})
                    else:
                        return JsonResponse({'test': 'test'})
                elif request.GET['action'] == 'form':
                    zapr = dict(request.__dict__['GET'])
                    org = zapr.get('org', None)
                    dep = zapr.get('dep', None)
                    cat = zapr.get('cat[]', None)
                    dates = zapr.get('date', None)
                    q1 = []
                    q2 = []
                    if dep[0] != 'None' and dep[0] != None:
                        q1 = []
                        q1.append(Q())
                        depza = Department.objects.filter(pk=int(dep[0]))
                        q1.append(Q(curat__in=depza))
                    elif org[0] != 'None' and org[0] != None:
                        temp = Curator.objects.filter(pk=int(org[0]))
                        q1.append(Q(org__in=temp))
                        q1.append(Q())
                    else:
                        q1 = None
                    if cat:
                        temp = []
                        for i in cat:
                            temp.append(int(i))
                        catza = Category.objects.filter(pk__in=tuple(temp))
                        q2.append(Q(temat__in=catza))
                    else:
                        q2.append(Q())
                    if dates != ['']:
                        temp = dates[0].split('-')
                        dateza = date(int(temp[0]), int(temp[1]), int(temp[2]))
                        q2.append(Q(dateotv=dateza))
                    else:
                        q2.append(Q())
                    term = ''
                    prob = ''
                    if q1:
                        term = Term.objects.filter(q1[0] & q1[1])
                        prob = Problem.objects.filter(
                            q2[0] & q2[1] & Q(terms__in=term) & (Q(visible='1') & Q(statussys='1')))
                    else:
                        prob = Problem.objects.filter(q2[0] & q2[1] & (Q(visible='1') & Q(statussys='1')))
                    serial = ProblemsSerializer(prob, many=True)
                    return JsonResponse(serial.data, safe=False)
                else:
                    return JsonResponse({'test': 'test'})
            else:
                content = {}
                content['form'] = {}
                content['form']['org'] = Curator.objects.all().exclude(name='Территориальное управление')
                content['form']['category'] = Category.objects.all()
                return render(request, 'problem/zapros.html', {'content': content})
        else:
            return redirect('index')


def analysis(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            content = {}
            if 'cate' in request.POST:
                kolvo = {}
                a = ''
                b = ''
                nowdatetime = datetime.now()
                nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
                if request.POST['cate'] == '1':
                    temp = prob_func('moderator')()
                    temp(request=request, action='todayproblem')
                    a = temp.prob
                    b = Term.objects.filter(problem__in=a, date=nowdate)
                    content['type'] = {'id': 1, 'text': 'Анализ сегоднящних обращений'}
                elif request.POST['cate'] == '2':
                    temp = prob_func('moderator')()
                    temp(request=request, action='prosrproblem')
                    a = temp.prob
                    b = Term.objects.filter(problem__in=a,
                                            date__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
                    content['type'] = {'id': 2, 'text': 'Анализ просроченных обращений'}
                content['data'] = []
                for i in b:
                    content['data'].append({'nomdobr': i.problem.nomdobr, 'dateotv': i.problem.dateotv.strftime('%d.%m.%Y'), 'status': i.problem.status.name, 'pk': i.pk, 'date': i.date.strftime('%d.%m.%Y')})
                kolvo['all'] = f'<h4>Всего обращений: <b>{len(a)}</b></h4>'
                kolvo['naz'] = f'<h4>По дате назначений: <b>{len(b)}</b></h4>'
                kolvo['prob'] = f'<h4>По дате обращений: <b>{len(a) - len(b)}</b></h4>'
                content['kolvo'] = kolvo
                return JsonResponse(content)
            else:
                return JsonResponse(content)
        else:
            return render(request, 'problem/analysis.html')
