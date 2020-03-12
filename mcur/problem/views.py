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

#reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.units import mm

# other
from .models import Problem, Curator, Term, Answer, Image, Status, Termhistory, Department, Person, Category, UserProfile
from parsers.models import ActionHistory, Action, Parser
from .tables import ProblemTable, ParsTable, UserTable
from .forms import (PrAdd, TermForm, AnswerForm,ResolutionForm, CreateUser)
from .filter import ProblemListView, ProblemFilter
from datetime import date, timedelta, datetime
import xlwt
import mcur.settings as settings
import random
import os

chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('__all__')


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


class ActionObject(object):
    def __init__(self, title, nom, message):
        self.title = title
        self.nom = nom
        self.message = message


@api_view(['POST'])
def api_action(request):
    if request.method == 'POST':
        #nowdatetime = datetime.now()
        #nowdate = datetime.date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        if request.POST['action'] == '1':
            title = 'Скрытие жалоб'
            status = ['Закрыто', 'Получен ответ', 'Решено']
            status2 = ['На рассмотрении', 'На уточнении', 'Премодерация']
            allprob = 0
            prob = Problem.objects.filter(Q(visible='1') & (Q(status__name=status[0]) | Q(status__name=status[1]) | Q(status__name=status[2])))
            allprob += len(prob)
            for i in prob:
                i.visible = '0'
                i.save()
            prob = Problem.objects.filter(Q(visible='1') & (Q(status__name=status2[0]) | Q(status__name=status2[1]) | Q(status__name=status2[2])))
            allprob += len(prob)
            for i in prob:
                i.visible = '2'
                i.save()
            mes = f'''Успешно выполнено!
Количество исправленных жалоб: {allprob}'''
            nom = 0
        elif request.POST['action'] == '2':
            a = ActionHistory()
            a.act = Action.objects.get(nact='2')
            a.arg = 'all'
            a.save()
            title = 'Добавление задачи'
            mes = f'''Успешно выполнено!
            Задание запущено.'''
            nom = 0
        elif request.POST['action'] == '3':
            a = ActionHistory()
            a.act = Action.objects.get(nact='8')
            a.save()
            title = 'Добавление задачи'
            mes = f'''Успешно выполнено!
            Задание запущено.'''
            nom = 0
        elif request.POST['action'] == '4':
            #date = nowdate - timedelta(7)
            #tempdate = ''
            a = ActionHistory()
            a.act = Action.objects.get(nact='8')

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
<p>Вам направлена задача сроком до {date}. На жалобу <a href='https://skiog.ru/problem/{nomd}'>№{nomd}</a></p>
<p></p>
<p>______________<p> 
<p>Администрация информационной системы skiog.ru </p>          
'''
    emai = email
    send_mail('SKIOG', None, 'noreply@skiog.ru', [emai], fail_silently=False, html_message=data)


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
            if not userlk.has_perm('problem.user_moderator'):
                q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
                terms = Termhistory.objects.filter(q1)
                if userlk.userprofile.dep == None:
                    q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
                terms1 = Term.objects.filter((Q(resolutions__in=terms) | q1) & (Q(status='0') | Q(status='1')))
                prob = Problem.objects.filter(terms__in=terms1, visible='1', statussys='1')
            else:
                #term = Term.objects.filter(Q(status='0') & Q(status='1'))
                prob = Problem.objects.filter(visible='1')
            filterall = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filterall.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filterall
            context['table'] = table
            context['name'] = 'Все жалобы'
            context['dop'] = f'Всего: {len(filterall.qs)}.'
            context['title'] = 'Все жалобы'
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
            prob = Problem.objects.filter(visible='1', statussys='2')
            if not self.request.user.has_perm('problem.user_moderator'):
                return redirect('index')
            filterno = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filterno.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filterno
            context['table'] = table
            context['name'] = 'Не распределенные жалобы'
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
                q1 = (Q(status='0') | Q(status='1')) & Q(date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
                q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
                q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(status__in=Status.objects.filter(name='Указан срок')))
                termas = Term.objects.filter(q1)
                prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
            elif userlk.has_perm('problem.user_executor'):
                if userlk.userprofile.dep == None:
                    q1 = Q(curatuser=userlk)
                    termas = Termhistory.objects.filter(q1)
                    q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
                else:
                    q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
                    termas = Termhistory.objects.filter(q1)
                q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
                termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
                q2 = Q(visible='1')
                q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
                prob = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)
            filterpodx = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filterpodx.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filterpodx
            context['table'] = table
            context['name'] = 'Подходит срок жалоб'
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
                q1 = (Q(status='0') | Q(status='1')) & Q(date__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
                q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
                q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(status__in=Status.objects.filter(name='Указан срок')))
                termas = Term.objects.filter(q1)
                prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
            elif userlk.has_perm('problem.user_executor'):
                q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
                termas = Termhistory.objects.filter(q1)
                if userlk.userprofile.dep == None:
                    q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
                q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(date(2019, 1, 1), nowdate - timedelta(1)))
                termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
                q2 = Q(visible='1')
                q21 = Q(dateotv__range=(date(2019, 1, 1), nowdate - timedelta(1)))
                prob = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)
            filterpros = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filterpros.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filterpros
            context['table'] = table
            context['name'] = 'Просроченные жалобы'
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
                q1 = (Q(status='0') | Q(status='1')) & Q(date=nowdate)
                q21 = Q(dateotv=nowdate)
                q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(status__in=Status.objects.filter(name='Указан срок')))
                termas = Term.objects.filter(q1)
                prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
            elif userlk.has_perm('problem.user_executor'):
                q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
                termas = Termhistory.objects.filter(q1)
                if userlk.userprofile.dep == None:
                    q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
                q2 = (Q(status='0') | Q(status='1')) & Q(date=nowdate)
                termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
                q2 = Q(visible='1')
                q21 = Q(dateotv=nowdate)
                prob = Problem.objects.filter((Q(terms__in=termas1)| q21) & q2)
            filtertodo = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filtertodo.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filtertodo
            context['table'] = table
            context['name'] = 'Жалобы на сегодня'
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
                nowdatetime = datetime.now()
                nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
                q1 = Q(curatuser=userlk)
                termas = Termhistory.objects.filter(q1)
                termas1 = Term.objects.filter(q1 | Q(resolutions__in = termas))
                prob = Problem.objects.filter(Q(terms__in=termas1))
                filterme = ProblemFilter(self.request.GET, queryset=prob)
                table = ProblemTable(filterme.qs)
                RequestConfig(self.request, ).configure(table )
                context['filter'] = filterme
                context['table'] = table
                context['name'] = 'Мои жалобы'
                context['dop'] = f'Всего: {len(filterme.qs)}.'
                context['title'] = 'Мои жалобы'
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
                    dep = Department.objects.filter(name=userr.userprofile.dep.name)
                    userorg = Person.objects.filter(userprofile__dep__in=dep)
                resform = ResolutionForm(curat_qs=dep, curatuser_qs=userorg)
                return render(request, 'problem/problem.html', {'answeradd': answeradd, 'formadd': termadd, 'np': prob, 'terms': terms, 'resform': resform})
            else:
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
                    messages.warning(request, 'Данная жалоба существует.')
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


def lk(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        userlk = User.objects.get(username=request.user.username)
        kolvo = {}
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        if request.user.has_perm('problem.user_moderator'):
            kolvo['kolall'] = len(Problem.objects.filter(visible='1'))
            kolvo['kolno'] = len(Problem.objects.filter(visible='1', statussys='2'))
            #Подходит срок
            q1 = (Q(status='0') | Q(status='1')) & Q(date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
            q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate+timedelta(4)))
            q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(status__in=Status.objects.filter(name='Указан срок')))
            termas = Term.objects.filter(q1)
            termas2 = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
            kolvo['podx'] = len(termas2)
            #Просроченные
            q1 = (Q(status='0') | Q(status='1')) & Q(date__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
            q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
            q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(status__in=Status.objects.filter(name='Указан срок')))
            termas = Term.objects.filter(q1)
            termas2 = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
            kolvo['prosr'] = len(termas2)
            #На сегодня
            q1 = (Q(status='0') | Q(status='1')) & Q(date=nowdate)
            q21 = Q(dateotv = nowdate)
            q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(status__in=Status.objects.filter(name='Указан срок')))
            termas = Term.objects.filter(q1)
            termas2 = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
            kolvo['today'] = len(termas2)
            #Мои
            #q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            #if userlk.userprofile.dep == None:
            q1 = Q(curatuser=userlk)
            termas = Term.objects.filter(q1)
            termas2 = Problem.objects.filter(Q(terms__in=termas))
            kolvo['me'] = len(termas2)
            kolvo['kolclose'] = len(Problem.objects.filter(visible='1', statussys='2', terms__answers__user=userlk))
        elif request.user.has_perm('problem.user_executor'):
            #1 блок ответы
            q1 = Q(user=userlk)
            termas = Answer.objects.filter(q1)
            termas2 = Term.objects.filter(answers__in=termas)
            termas3 = Problem.objects.filter(visible='1', terms__in=termas2)
            kolvo['kolclose'] = len(termas3)
            #2 блок всего не закрытых жалоб
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            if userlk.userprofile.dep == None:
                q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
            termas2 = Term.objects.filter((q1 | Q(resolutions__in=termas)) & (Q(status='0') | Q(status='1')))
            termas3 = Problem.objects.filter((Q(visible='1') & Q(statussys='1')) & Q(terms__in=termas2))
            kolvo['kolall'] = len(termas3)
            #3 Подходит срок жалоб
            if userlk.userprofile.dep == None:
                q1 = Q(curatuser=userlk)
                termas = Termhistory.objects.filter(q1)
                q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
            else:
                q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
                termas = Termhistory.objects.filter(q1)
            q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
            termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
            q2 = Q(visible='1')
            q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
            termas2 = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)
            kolvo['podx'] = len(termas2)
            #4 Блок жалоб на сегодня
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            if userlk.userprofile.dep == None:
                q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
            q2 = (Q(status='0') | Q(status='1')) & Q(date=nowdate)
            termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
            q2 = Q(visible='1') & Q(statussys='1')
            q21 = Q(dateotv=nowdate)
            termas2 = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)
            kolvo['today'] = len(termas2)
            # 5 Просроченные жалобы
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            if userlk.userprofile.dep == None:
                q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
            q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(date(2019, 1, 1), nowdate-timedelta(1)))
            termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
            q2 = Q(visible='1') & Q(statussys='1')
            q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
            termas2 = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)
            kolvo['prosr'] = len(termas2)
        return render(request, 'problem/lk.html', {'kolvo': kolvo})


def closedproblem(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        name = 'Закрытые жалобы'
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
        rows = Problem.objects.filter(Q(visible='1')).values_list('pk', 'nomdobr', 'temat__name', 'podcat__name',
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
                print(request.POST)
                password = ''
                for i in range(8):
                    password += random.choice(chars)
                user = User.objects.create_user(request.POST['username'], request.POST['email'], password)
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
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        dates = {}
        dates['min'] = []
        for i in range(6, 0, -1):
            dates['min'].append(nowdate-timedelta(i))
        dates['min'].append(nowdate)
        dates['plus'] = []
        for i in range(0,7):
            dates['plus'].append(nowdate+timedelta(i))
        kolvo = {}
        kolvo['terms'] = []
        kolvo['problems'] = []
        for i in dates['min']:
            kolvo['terms'].append(len(Term.objects.filter(datecre=i)))
        for i in dates['plus']:
            q1 = Q(status='0') & Q(date=i)
            q21 = Q(dateotv=i)
            q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
                status__in=Status.objects.filter(name='Указан срок')))
            termas = Term.objects.filter(q1)
            termas2 = Problem.objects.filter(Q(terms__in=termas) | q21 & q22)
            kolvo['problems'].append(len(termas2))
        return render(request, 'problem/dashboard.html', {'dates': dates, 'kolvo': kolvo})

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
        url = 'http://127.0.0.1:8000/problem/'
        barcode_string = f'<font name="Times" size="16">Жалоба №<a href="{url}{prob.nomdobr}" underline="True">{prob.nomdobr}</a></font>'
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
        barcode_string = f'''<font name="Times" size="16">Текс жалобы: 
    </font> <font name="Times" size="14"> 
    <p>{prob.text}</p>
    </font>'''
        p = Paragraph(barcode_string, style=style["Normal"])
        print(p)
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
            content['status'] = ['Закрыто', 'Получен ответ', 'Решено', 'На рассмотрении', 'На уточнении', 'Премодерация']
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
            parser = Parser.objects.all()
            table = ParsTable(parser)
            RequestConfig(request, ).configure(table)
            return render(request, 'problem/statandact.html', {'parsers': table, 'content': content})
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