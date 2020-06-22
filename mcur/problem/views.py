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
from .logick import lk_dispatcher, lk_executor, lk_moderator, lk_ty
from mcur import settings


# other
from datetime import date, timedelta, datetime
from sys import platform
from operator import itemgetter
import xlwt
import random
import os
import logging


logger = logging.getLogger('django.server')
logger_mail = logging.getLogger('django.request')
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


@api_view(['POST'])
def api_report(request):
    if request.user.has_perm('problem.user_moderator'):
        if request.method == 'POST':
            nowdatetime = datetime.now()
            if request.POST['report'] == '1':
                if 'linux' in platform.lower():
                    temp = request.POST['datefrom'].split('-')
                    datefrom = date(int(temp[0]), int(temp[1]), int(temp[2]))
                    temp = request.POST['datebefore'].split('-')
                    datebefore = date(int(temp[0]), int(temp[1]), int(temp[2]))
                else:
                    datefrom = date.fromisoformat(request.POST['datefrom'])
                    datebefore = date.fromisoformat(request.POST['datebefore'])
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('problems')
                row_num = 0
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес',
                           'Дата жалобы',
                           'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                font_style = xlwt.XFStyle()
                rows = Problem.objects.filter(datecre__range=(datefrom, datebefore)).values_list('pk', 'nomdobr',
                                                        'temat__name', 'podcat__name', 'text', 'adres', 'datecre',
                                                         'dateotv', 'status__name', 'statussys')
                for row in rows:
                    row_num += 1
                    for col_num in range(len(row)):
                        if col_num == 6 or col_num == 7:
                            ws.write(row_num, col_num, f'{row[col_num].day}.{row[col_num].month}.{row[col_num].year}',
                                     font_style)
                        else:
                            ws.write(row_num, col_num, row[col_num], font_style)
                name = f'{nowdatetime.day}{nowdatetime.month}{nowdatetime.year}{nowdatetime.hour}{nowdatetime.minute}.xls'
                wb.save(f'{settings.MEDIA_ROOT}xls/{name}')
                if 'linux' in platform.lower():
                    url = f'https://skiog.ru/media/xls/{name}'
                else:
                    url = f'http://127.0.0.1:8000/media/xls/{name}'
                title = 'Успешно'
                mes = 'Отчет подготовлен!'
                nom = 0
                cont = {'url': url, 'title': title, 'message': mes, 'nom': nom}
                return JsonResponse(cont)
            if request.POST['report'] == '2':
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('problems')
                row_num = 0
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес',
                           'Дата жалобы',
                           'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                font_style = xlwt.XFStyle()
                rows = Problem.objects.filter(visible='1').values_list('pk', 'nomdobr', 'temat__name', 'podcat__name',
                                                         'text', 'adres', 'datecre',
                                                         'dateotv', 'status__name', 'statussys')
                for row in rows:
                    row_num += 1
                    for col_num in range(len(row)):
                        if col_num == 6 or col_num == 7:
                            ws.write(row_num, col_num, f'{row[col_num].day}.{row[col_num].month}.{row[col_num].year}',
                                     font_style)
                        else:
                            ws.write(row_num, col_num, row[col_num], font_style)
                name = f'{nowdatetime.day}{nowdatetime.month}{nowdatetime.year}{nowdatetime.hour}{nowdatetime.minute}.xls'
                wb.save(f'{settings.MEDIA_ROOT}xls/{name}')
                if 'linux' in platform.lower():
                    url = f'https://skiog.ru/media/xls/{name}'
                else:
                    url = f'http://127.0.0.1:8000/media/xls/{name}'
                title = 'Успешно'
                mes = 'Отчет подготовлен!'
                nom = 0
                cont = {'url': url, 'title': title, 'message': mes, 'nom': nom}
                return JsonResponse(cont)
            if request.POST['report'] == '3':
                if 'linux' in platform.lower():
                    temp = request.POST['datefrom'].split('-')
                    datefrom = date(int(temp[0]), int(temp[1]), int(temp[2]))
                    temp = request.POST['datebefore'].split('-')
                    datebefore = date(int(temp[0]), int(temp[1]), int(temp[2]))
                else:
                    datefrom = date.fromisoformat(request.POST['datefrom'])
                    datebefore = date.fromisoformat(request.POST['datebefore'])
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('problems')
                row_num = 0
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                font_style.alignment.horz = 0x02
                cats = Category.objects.all()
                tempdate = []
                notes = []
                days = datebefore - datefrom
                tempdate.append(datefrom)
                notes.append('Наименование')
                notes.append(datefrom.strftime('%d.%m.%Y'))
                first_col = ws.col(0)
                first_col.width = 256 * 20
                for i in range(days.days):
                    td = tempdate[-1] + timedelta(1)
                    tempdate.append(td)
                    notes.append(td.strftime('%d.%m.%Y'))
                    col = ws.col(i+1)
                    col.width = 256 * 10
                col = ws.col(days.days+1)
                col.width = 256 * 10
                col = ws.col(days.days + 2)
                col.width = 256 * 10
                notes.append('Итого')
                temp = []
                for i in cats:
                    c = []
                    d = 0
                    c.append(i.name)
                    for j in tempdate:
                        ea = len(Problem.objects.filter(temat=i, datecre=j))
                        d += ea
                        c.append(ea)
                    c.append(d)
                    temp.append(c)
                columns = notes
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                font_style = xlwt.XFStyle()
                temp = sorted(temp, key=itemgetter(days.days+2), reverse=True)
                rows = temp
                for row in rows:
                    row_num += 1
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                name = f'cats-{nowdatetime.day}{nowdatetime.month}{nowdatetime.year}{nowdatetime.hour}{nowdatetime.minute}.xls'
                wb.save(f'{settings.MEDIA_ROOT}xls/{name}')
                if 'linux' in platform.lower():
                    url = f'https://skiog.ru/media/xls/{name}'
                else:
                    url = f'http://127.0.0.1:8000/media/xls/{name}'
                title = 'Успешно'
                mes = 'Отчет подготовлен!'
                nom = 0
                cont = {'url': url, 'title': title, 'message': mes, 'nom': nom}
                return JsonResponse(cont)
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
    if request.method == 'GET':
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


def ProblemOrgView(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.has_perm('problem.user_moderator'):
            prob = []
            term = []
            cur = Curator.objects.all().exclude(name='Территориальное управление')
            if request.GET:
                if request.GET['organization']:
                    temp = request.GET['organization']
                    term = Term.objects.filter(org__pk=int(temp))
                    prob = Problem.objects.filter(visible='1', terms__in=term).distinct()
                else:
                    prob = Problem.objects.filter(visible='1').exclude(terms=None)
            else:
                prob = Problem.objects.filter(visible='1').exclude(terms=None)
            table = ProblemTable(prob)
            RequestConfig(request, ).configure(table)
            filter2 = cur
            table = table
            name = 'Обращения по организациям'
            dop = f'Всего: {len(prob)}.'
            title = 'Обращения по организациям'
            return render(request, "problem/allproblem.html", {'table': table, 'name': name, 'dop': dop, 'title': title, 'filter2': filter2})
        else:
            return redirect('index')


def export_xls(problem):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="problems.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('problems')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес', 'Дата жалобы',
               'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = problem.values_list('pk', 'nomdobr', 'temat__name', 'podcat__name',
                                                                             'text', 'adres', 'datecre',
                                                                             'dateotv', 'status__name', 'statussys')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 6 or col_num == 7:
                ws.write(row_num, col_num, f'{row[col_num].day}.{row[col_num].month}.{row[col_num].year}', font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


class ProblemListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            if userlk.has_perm('problem.user_moderator'):
                prob = lk_moderator.b3(request=self.request, act=2)
            elif userlk.has_perm('problem.user_dispatcher'):
                prob = lk_dispatcher.b1(request=self.request, act=2)
            elif userlk.has_perm('problem.user_executor'):
                prob = lk_executor.b2(request=self.request, act=2)
            elif userlk.has_perm('problem.user_ty'):
                prob = lk_ty.b1(request=self.request, act=2)
            filterall = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filterall.qs)
            RequestConfig(self.request, ).configure(table)
            context['filter'] = filterall
            context['table'] = table
            context['name'] = 'Все обращения'
            context['dop'] = f'Всего: {len(filterall.qs)}.'
            context['title'] = 'Все обращения'
        return context


class ProblemNoListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemNoListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        else:
            action = self.request.GET.get('action', None)
            prob = lk_moderator.b2(request=self.request, act=2)
            if not self.request.user.has_perm('problem.user_moderator'):
                return redirect('index')
            filterno = ProblemFilter(self.request.GET, queryset=prob)
            if action == 'export_xls':
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="problems.xls"'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('problems')
                row_num = 0
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес',
                           'Дата жалобы', 'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                font_style = xlwt.XFStyle()
                rows = filterno.queryset.values_list('pk', 'nomdobr', 'temat__name', 'podcat__name',
                                           'text', 'adres', 'datecre',
                                           'dateotv', 'status__name', 'statussys')
                for row in rows:
                    row_num += 1
                    for col_num in range(len(row)):
                        if col_num == 6 or col_num == 7:
                            ws.write(row_num, col_num, f'{row[col_num].day}.{row[col_num].month}.{row[col_num].year}',
                                     font_style)
                        else:
                            ws.write(row_num, col_num, row[col_num], font_style)
                wb.save(response)
                return response
            table = ProblemTable(filterno.qs)
            RequestConfig(self.request, ).configure(table)
            context['filter'] = filterno
            context['table'] = table
            context['name'] = 'Не распределенные обращения'
            context['dop'] = f'Всего: {len(filterno.qs)}.'
            context['title'] = 'Не распределенные'
        return context


class ProblemPodxListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemPodxListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            nowdatetime = datetime.now()
            nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
            if userlk.has_perm('problem.user_moderator'):
                prob = lk_moderator.b5(request=self.request, act=2)
            elif userlk.has_perm('problem.user_dispatcher'):
                prob = lk_dispatcher.b3(request=self.request, act=2)
            elif userlk.has_perm('problem.user_executor'):
                prob = lk_executor.b3(request=self.request, act=2)
            filterpodx = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filterpodx.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filterpodx
            context['table'] = table
            context['name'] = 'Подходит срок обращения'
            context['dop'] = f'Всего: {len(filterpodx.qs)}.'
            context['title'] = 'Подходит срок'
        return context


class ProblemProsrListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemProsrListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            nowdatetime = datetime.now()
            nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
            if userlk.has_perm('problem.user_moderator'):
                prob = lk_moderator.b7(request=self.request, act=2)
            elif userlk.has_perm('problem.user_dispatcher'):
                prob = lk_dispatcher.b5(request=self.request, act=2)
            elif userlk.has_perm('problem.user_executor'):
                prob = lk_executor.b5(request=self.request, act=2)
            filterpros = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filterpros.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filterpros
            context['table'] = table
            context['name'] = 'Просроченные обращения'
            context['dop'] = f'Всего: {len(filterpros.qs)}.'
            context['title'] = 'Просроченные'
        return context


class ProblemTodayListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemTodayListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            nowdatetime = datetime.now()
            nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
            if userlk.has_perm('problem.user_moderator'):
                prob = lk_moderator.b6(request=self.request, act=2)
            elif userlk.has_perm('problem.user_dispatcher'):
                prob = lk_dispatcher.b4(request=self.request, act=2)
            elif userlk.has_perm('problem.user_executor'):
                prob = lk_executor.b4(request=self.request, act=2)
            filtertodo = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filtertodo.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filtertodo
            context['table'] = table
            context['name'] = 'Обращения на сегодня'
            context['dop'] = f'Всего: {len(filtertodo.qs)}.'
            context['title'] = 'На сегодня'
        return context


class ProblemMeListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemMeListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            if userlk.has_perm('problem.user_moderator'):
                prob = lk_moderator.b4(request=self.request, act=2)
            elif userlk.has_perm('problem.user_executor'):
                prob = lk_executor.b6(request=self.request, act=2)
            filterme = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filterme.qs)
            RequestConfig(self.request, ).configure(table)
            context['filter'] = filterme
            context['table'] = table
            context['name'] = 'Мои обращения'
            context['dop'] = f'Всего: {len(filterme.qs)}.'
            context['title'] = 'Мои обращения'
        return context


class ProblemTyListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemTyListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            if userlk.has_perm('problem.user_moderator'):
                prob = lk_moderator.b8(request=self.request, act=2)
                filterme = ProblemFilter(self.request.GET, queryset=prob)
                table = ProblemTable(filterme.qs)
                RequestConfig(self.request, ).configure(table )
                context['filter'] = filterme
                context['table'] = table
                context['name'] = 'Обращения без ТУ'
                context['dop'] = f'Всего: {len(filterme.qs)}.'
                context['title'] = 'Обращения без ТУ'
        return context


class ProblemFuListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemFuListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            if userlk.has_perm('problem.user_moderator'):
                prob = lk_moderator.b9(request=self.request, act=2)
                filterme = ProblemFilter(self.request.GET, queryset=prob)
                table = ProblemTable(filterme.qs)
                RequestConfig(self.request, ).configure(table )
                context['filter'] = filterme
                context['table'] = table
                context['name'] = 'Обещанные обращения'
                context['dop'] = f'Всего: {len(filterme.qs)}.'
                context['title'] = 'Обещанные обращения'
        return context


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


def termadd(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        prob = Problem.objects.get(pk=pk)
        title = 'Добавление назначения'
        if request.user.has_perm('problem.user_moderator'):
            if request.method == 'POST':
                formadd = TermForm(request.POST)
                if formadd.is_valid():
                    a = formadd.save()
                    nd = Problem.objects.get(pk=pk)
                    a.problem = nd
                    a.user = request.user
                    if a.further == False:
                        a.furtherdate = None
                    a.save()
                    nd.statussys = '1'
                    nd.save()
                    if a.curatuser:
                        temp = f'{a.date.day}.{a.date.month}.{a.date.year}'
                        #Mailsend(a.curatuser.email, temp, a.problem.nomdobr)
                    mes = 'Назначение успешно добавлено.'
                    nom = 0
                    a = ActionObject(title=title, nom=nom, message=mes)
                    serializer = ActionSerializer(a)
                    return JsonResponse(serializer.data, safe=False)
            else:
                mes = 'Ошибка, форма не прошла валидацию.'
                nom = 1
                a = ActionObject(title=title, nom=nom, message=mes)
                serializer = ActionSerializer(a)
                return JsonResponse(serializer.data, safe=False)
            #return render(request, 'problem/termadd.html', {'auth': True, 'formadd': formadd, 'np': prob, 'prob': prob})
        else:
            mes = 'Ошибка, не достаточно прав на создание назначения.'
            nom = 1
            a = ActionObject(title=title, nom=nom, message=mes)
            serializer = ActionSerializer(a)
            return JsonResponse(serializer.data, safe=False)


def delterm(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = 'Удаление назначения'
        if request.user.has_perm('problem.user_moderator'):
            if Term.objects.filter(pk=pk).exists():
                if request.method == 'POST':
                    b = Term.objects.get(pk=pk)
                    nd = b.problem
                    b.delete()
                    if len(nd.terms.all()) == 0:
                        nd.statussys = '2'
                        nd.save()
                    mes = 'Назначение удалено'
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
                mes = 'Ошибка, данного назначения не найдено.'
                nom = 1
                a = ActionObject(title=title, nom=nom, message=mes)
                serializer = ActionSerializer(a)
                return JsonResponse(serializer.data, safe=False)
        else:
            mes = 'Ошибка, не достаточно прав на удаление назначения.'
            nom = 1
            a = ActionObject(title=title, nom=nom, message=mes)
            serializer = ActionSerializer(a)
            return JsonResponse(serializer.data, safe=False)


def delty(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = 'Удаление ТУ обращения'
        if request.user.has_perm('problem.user_moderator'):
            if Term.objects.filter(pk=pk).exists():
                if request.method == 'POST':

                    mes = 'Удалено'
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
                mes = 'Ошибка'
                nom = 1
                a = ActionObject(title=title, nom=nom, message=mes)
                serializer = ActionSerializer(a)
                return JsonResponse(serializer.data, safe=False)
        else:
            mes = 'Ошибка, не достаточно прав на удаление.'
            nom = 1
            a = ActionObject(title=title, nom=nom, message=mes)
            serializer = ActionSerializer(a)
            return JsonResponse(serializer.data, safe=False)


def lk(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        nowdatetime = datetime.now()
        if request.method == 'POST':
            if request.user.has_perm('problem.user_moderator'):
                if request.POST['box'] == 'box1':# Ответы
                    kolvo = lk_moderator.b1(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box2':# Не рапсред. обращения
                    kolvo = lk_moderator.b2(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box3':# Все обращения
                    kolvo = lk_moderator.b3(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box4':# Мои обращения
                    kolvo = lk_moderator.b4(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box5':# Подходит срок
                    kolvo = lk_moderator.b5(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box6':# Обращения на сегодня
                    kolvo = lk_moderator.b6(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box7':# Просроченные
                    kolvo = lk_moderator.b7(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box8':# ТУ лист
                    kolvo = lk_moderator.b8(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box9':# ТУ лист
                    kolvo = lk_moderator.b9(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                else:
                    return JsonResponse({'mes': 'error'})
            elif request.user.has_perm('problem.user_dispatcher'):
                if request.POST['box'] == 'box1':  # Ответы
                    kolvo = lk_dispatcher.b2(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box3':  # Все обращения
                    kolvo = lk_dispatcher.b1(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box5':  # Подходит срок
                    kolvo = lk_dispatcher.b3(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box6':  # Обращения на сегодня
                    kolvo = lk_dispatcher.b4(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box7':  # Просроченные
                    kolvo = lk_dispatcher.b5(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
            elif request.user.has_perm('problem.user_executor'):
                if request.POST['box'] == 'box1':  # Ответы
                    kolvo = lk_executor.b1(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box3':  # Все обращения
                    kolvo = lk_executor.b2(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box5':  # Подходит срок
                    kolvo = lk_executor.b3(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box6':  # Обращения на сегодня
                    kolvo = lk_executor.b4(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box7':  # Просроченные
                    kolvo = lk_executor.b5(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                elif request.POST['box'] == 'box8':  # Просроченные
                    kolvo = lk_executor.b6(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                else:
                    return JsonResponse({'mes': 'error'})
            elif request.user.has_perm('problem.user_ty'):
                if request.POST['box'] == 'box3':  # Все обращения
                    kolvo = lk_ty.b1(request=request, act=1)
                    return JsonResponse({'boxn': request.POST['box'], 'kolvo': kolvo, 'mes': 'succes'})
                else:
                    return JsonResponse({'mes': 'error'})
        return render(request, 'problem/lk.html')


def closedproblem(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        name = 'Закрытые обращения'
        userlk = User.objects.get(username=request.user.username)
        otv = Answer.objects.filter(user=userlk)
        prob = Problem.objects.filter(terms__answers__in = otv, visible = '1')
        kolvo = len(prob)
        config = RequestConfig(request, paginate={'paginator_class': LazyPaginator, 'per_page': 10})
        table = ProblemTable(prob)
        config.configure(table)
        return render(request, 'problem/allproblem.html', {'table': table, 'name': name, 'kolvo': kolvo})


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


def exportxls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="problems.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('problems')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес', 'Дата жалобы',
               'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    userlk = User.objects.get(username=request.user.username)
    if request.user.has_perm('problem.user_moderator'):
        #prob = filterall = ProblemFilter(request.GET, queryset=prob)
        rows = Problem.objects.all().values_list('pk', 'nomdobr', 'temat__name', 'podcat__name',
                                                                             'text', 'adres', 'datecre',
                                                                             'dateotv', 'status__name', 'statussys')
    elif request.user.has_perm('problem.user_dispatcher'):
        if userlk.userprofile.dep:
            q1 = Q(terms__org=userlk.userprofile.org) | Q(terms__curat=userlk.userprofile.dep) | Q(terms__curatuser=userlk)
            q2 = Q(terms__resolutions__curat=userlk.userprofile.dep) | Q(terms__resolutions__curatuser=userlk)
        else:
            q1 = Q(terms__org=userlk.userprofile.org) | Q(terms__curatuser=userlk)
            q2 = Q(terms__resolutions__curatuser=userlk)
        rows = Problem.objects.filter(Q(visible='1'), (q1 | q2)).values_list('pk', 'nomdobr', 'temat__name',
                                                                             'podcat__name', 'text', 'adres', 'datecre',
                                                                             'dateotv', 'status__name', 'statussys')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 6 or col_num == 7:
                ws.write(row_num, col_num, f'{row[col_num].day}.{row[col_num].month}.{row[col_num].year}', font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


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


def addparsing(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = 'Обновление проблемы'
        if request.user.has_perm('problem.user_moderator'):
            if request.method == 'POST':

                hist = ActionHistory(act=Action.objects.get(nact='2'), arg=pk, status='0')
                hist.save()
                mes = 'Проблема отправлена на обновление.'
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
            mes = 'Ошибка, не достаточно прав на обновление проблемы.'
            nom = 1
            a = ActionObject(title=title, nom=nom, message=mes)
            serializer = ActionSerializer(a)
            return JsonResponse(serializer.data, safe=False)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.has_perm('problem.user_moderator'):
            nowdatetime = datetime.now()
            nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
            dates = {}
            notes = []
            if request.method == 'POST':
                if request.POST['chart'] == 'chart1':
                    tempdate = []
                    for i in range(6, 0, -1):
                        tempdate.append(nowdate-timedelta(i))
                    tempdate.append(nowdate)
                    kolvo = []
                    for i in tempdate:
                        kolvo.append(len(Term.objects.filter(datecre=i)))
                elif request.POST['chart'] == 'chart2':
                    tempdate = []
                    for i in range(0, 7):
                        tempdate.append(nowdate + timedelta(i))
                    kolvo = []
                    for i in tempdate:
                        q1 = Q(status='0') & Q(date=i)
                        q21 = Q(dateotv=i)
                        q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
                            status__in=Status.objects.filter(name='Указан срок')))
                        termas = Term.objects.filter(q1)
                        termas2 = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
                        kolvo.append(len(termas2))
                elif request.POST['chart'] == 'chart3':
                    temporg = Curator.objects.all().exclude(name='Территориальное управление')
                    tempdate = []
                    kolvo = []
                    for i in temporg:
                        tempdate.append(i.name)
                        kolvo.append(len(Term.objects.filter((Q(org=i) | Q(curat__org=i)) & Q(problem__visible='1'))))
                elif request.POST['chart'] == 'chart4':
                    tempty = Minis.objects.all()
                    tempdate = []
                    kolvo = []
                    for i in tempty:
                        tempdate.append(i.name)
                        te = len(Problem.objects.filter(Q(ciogv=i) & Q(visible='1')))
                        kolvo.append(te)
                    prob = Problem.objects.filter(Q(visible='1'))
                elif request.POST['chart'] == 'chart5':
                    tempdate = ''
                    author = Author.objects.all()
                    temp = {}
                    kolvo = []
                    for i in author:
                        temp[i.pk] = len(i.problems.all())
                    temp = sorted(temp.items(), key=itemgetter(1), reverse=True)
                    for i in range(25):
                        nom = temp[i][0]
                        autho = Author.objects.get(pk=nom)
                        a = {}
                        a['fio'] = autho.fio
                        a['email'] = autho.email
                        a['tel'] = autho.tel
                        a['kolvo'] = temp[i][1]
                        kolvo.append(a)
                elif request.POST['chart'] == 'chart6':
                    tempdate = []
                    for i in range(6, 0, -1):
                        tempdate.append(nowdate-timedelta(i))
                    tempdate.append(nowdate)
                    kolvo = []
                    for i in tempdate:
                        kolvo.append(len(Problem.objects.filter(datecre=i)))
                elif request.POST['chart'] == 'chart7':
                    cats = Category.objects.all()
                    kolvo = []
                    tempdate = []
                    notes = []
                    for i in range(4, 0, -1):
                        temp = nowdate - timedelta(i)
                        tempdate.append(temp)
                        notes.append(temp.strftime('%d.%m.%Y'))
                    tempdate.append(nowdate)
                    notes.append(nowdate.strftime('%d.%m.%Y'))
                    temp = {}
                    for j in cats:
                        temp[j.pk] = len(Problem.objects.filter(temat=j, datecre__range=[tempdate[0], tempdate[-1]]))
                    temp = sorted(temp.items(), key=itemgetter(1), reverse=True)
                    for i in range(5):
                        nom = temp[i][0]
                        cat = Category.objects.get(pk=nom)
                        a = {'nam': cat.name}
                        c = 1
                        for j in tempdate:
                            a[f'd{c}'] = len(Problem.objects.filter(temat=cat, datecre=j))
                            c += 1
                        kolvo.append(a)
                else:
                    return JsonResponse({'chart': 'error'})
                otv = {'label': tempdate, 'data': kolvo, 'chart': request.POST['chart'], 'notes': notes}
                return JsonResponse(otv)
            return render(request, 'problem/dashboard.html')
        else:
            redirect('index')


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


def term_approve(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = 'Утверждение назначения'
        if request.user.has_perm('problem.user_moderator'):
            if Term.objects.filter(pk=pk).exists():
                if request.method == 'POST':
                    term = Term.objects.get(pk=pk)
                    term.status = '2'
                    term.save()
                    mes = 'Назначение утверждено.'
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
                mes = 'Ошибка, данного назначения не существует.'
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


def addty(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = 'Добавление ТУ'
        if request.user.has_perm('problem.user_moderator'):
            if request.method == 'POST':
                if Problem.objects.filter(nomdobr=request.POST['prob']).exists():
                    proble = Problem.objects.get(nomdobr=request.POST['prob'])
                    proble.ciogv = Minis.objects.get(pk=request.POST['name'])
                    proble.save()
                    mes = 'Успешно, территориальное управление добавлено.'
                    nom = 0
                    a = ActionObject(title=title, nom=nom, message=mes)
                    serializer = ActionSerializer(a)
                    return JsonResponse(serializer.data, safe=False)
                else:
                    mes = 'Ошибка, данного обращения не существует.'
                    nom = 1
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


def changeterm(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = 'Изменение даты назначения'
        if request.user.has_perm('problem.user_moderator'):
            if request.method == 'POST':
                if 'view' in request.POST:
                    term = Term.objects.get(pk=request.POST['pk'])
                    content = {'date': term.date.strftime('%Y-%m-%d')}
                    return JsonResponse(content)
                elif 'change' in request.POST:
                    term = Term.objects.get(pk=request.POST['pk'])
                    ndate = request.POST['date'].split('-')
                    term.date = date(int(ndate[0]), int(ndate[1]), int(ndate[2]))
                    term.save()
                    mes = 'Изменение успешно.'
                    nom = 0
                    a = ActionObject(title=title, nom=nom, message=mes)
                    serializer = ActionSerializer(a)
                    return JsonResponse(serializer.data, safe=False)
            else:
                mes = 'Ошибка, не правильный запрос.'
                nom = 1
                a = ActionObject(title=title, nom=nom, message=mes)
                serializer = ActionSerializer(a)
                return JsonResponse(serializer.data, safe=False)
        else:
            mes = 'Ошибка, не достаточно прав на создание назначения.'
            nom = 1
            a = ActionObject(title=title, nom=nom, message=mes)
            serializer = ActionSerializer(a)
            return JsonResponse(serializer.data, safe=False)


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
                    a = lk_moderator.b6(request, 2)
                    b = Term.objects.filter(problem__in=a, date=nowdate)
                    content['type'] = {'id': 1, 'text': 'Анализ сегоднящних обращений'}
                elif request.POST['cate'] == '2':
                    a = lk_moderator.b7(request, 2)
                    b = Term.objects.filter(problem__in=a,
                                            date__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
                    content['type'] = {'id': 2, 'text': 'Анализ просроченных обращений'}
                kolvo['all'] = f'<h4>Всего обращений: <b>{len(a)}</b></h4>'
                kolvo['naz'] = f'<h4>По дате назначений: <b>{len(b)}</b></h4>'
                kolvo['prob'] = f'<h4>По дате обращений: <b>{len(a) - len(b)}</b></h4>'
                content['kolvo'] = kolvo
                return JsonResponse(content)
            else:
                return JsonResponse(content)
        else:
            return render(request, 'problem/analysis.html')
