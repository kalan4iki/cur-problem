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

# other
from .models import Problem, Curator, Term, Answer, Image, Status, Termhistory, Department
from parsers.models import ActionHistory, Action
from .tables import ProblemTable
from .forms import (PrAdd, TermForm, AnswerForm,ResolutionForm, CreateUser)
from .filter import ProblemListView, ProblemFilter
from datetime import date, timedelta, datetime
import xlwt
import mcur.settings as settings
import random

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
            prob = Problem.objects.filter(visible='1')
            userlk = User.objects.get(username=self.request.user.username)
            if not self.request.user.has_perm('problem.user_moderator'):
                q1 = Q(org=userlk.userprofile.org) | Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
                terms = Term.objects.filter(q1)
                prob = Problem.objects.filter(terms__in=terms, visible='1', statussys='1')
            filter = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filter.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filter
            context['table'] = table
            context['name'] = 'Все жалобы'
            context['dop'] = f'Всего: {len(filter.qs)}.'
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
            userlk = User.objects.get(username=self.request.user.username)
            if not self.request.user.has_perm('problem.user_moderator'):
                return redirect('index')
            filter = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filter.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filter
            context['table'] = table
            context['name'] = 'Не распределенные жалобы'
            context['dop'] = f'Всего: {len(filter.qs)}.'
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
                terms = Term.objects.filter(status='0', date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
                q1 = (Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(3))) & Q(
                    status=Status.objects.get(name='В работе')))
                q2 = Q(visible='1') | Q(statussys='1')
                prob = Problem.objects.filter(Q(terms__in=terms) | q1, q2)
            elif userlk.has_perm('problem.user_executor'):
                q1 = Q(status='0')
                q2 = Q(date__range=(nowdate, nowdate + timedelta(3)))
                q31 = Q(org=userlk.userprofile.org) | Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
                q32 = Q(resolutions__curat=userlk.userprofile.dep) | Q(resolutions__curatuser=userlk)
                q3 = (q31 | q32)
                terms = Term.objects.filter(q1, q2, q3)
                prob = Problem.objects.filter(terms__in=terms, visible='1', statussys='1')
            filter = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filter.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filter
            context['table'] = table
            context['name'] = 'Подходит срок жалоб'
            context['dop'] = f'Всего: {len(filter.qs)}.'
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
                terms = Term.objects.filter(status='0', date__range=(date(nowdatetime.year, 1, 1), nowdate))
                q1 = (Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate)) & Q(status=Status.objects.get(name='В работе')))
                q2 = Q(visible='1') | Q(statussys='1')
                prob = Problem.objects.filter(Q(terms__in=terms) | q1, q2)
            elif userlk.has_perm('problem.user_executor'):
                q1 = Q(status='0')
                q2 = Q(date__range=(date(nowdatetime.year, 1, 1), nowdate))
                q31 = Q(org=userlk.userprofile.org) | Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
                q32 = Q(resolutions__curat=userlk.userprofile.dep) | Q(resolutions__curatuser=userlk)
                q3 = (q31 | q32)
                terms = Term.objects.filter(q1, q2, q3)
                prob = Problem.objects.filter(terms__in=terms, visible='1', statussys='1')
            filter = ProblemFilter(self.request.GET, queryset=prob)
            table = ProblemTable(filter.qs)
            RequestConfig(self.request, ).configure(table )
            context['filter'] = filter
            context['table'] = table
            context['name'] = 'Просроченные жалобы'
            context['dop'] = f'Всего: {len(filter.qs)}.'
            context['title'] = 'Просроченные'
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
        if not request.user.has_perm(''):
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
                    userorg = User.objects.all()
                elif userr.has_perm('problem.user_dispatcher'):
                    dep = Department.objects.filter(org=userr.userprofile.org)
                    userorg = User.objects.filter(userprofile__org=userr.userprofile.org)
                elif userr.has_perm('problem.user_executor'):
                    dep = Department.objects.filter(name=userr.userprofile.dep.name)
                    userorg = User.objects.filter(userprofile__dep__in=dep)
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
                    return redirect("problem", pk=nd.nomdobr)
            else:
                formadd = TermForm()
            return render(request, 'problem/termadd.html', {'auth': True, 'formadd': formadd, 'np': prob, 'prob': prob})
        else:
            return render(request, 'problem/termadd.html', {'auth': False, 'np': prob, 'prob': prob})


def delterm(request, pk, pkp):
    b = Term.objects.get(pk=pk)
    nd = b.problem
    b.delete()
    if len(nd.terms.all()) == 0:
        nd.statussys = '2'
        nd.save()
    return redirect("problem", pk=nd.nomdobr)


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
            q1 = Q(status='0') & Q(date__range=(nowdate + timedelta(1), nowdate+timedelta(3)))
            q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate+timedelta(3))) & Q(
                status=Status.objects.get(name='В работе'))
            q22 = Q(visible='1') | Q(statussys='1')
            termas = Term.objects.filter(q1)
            termas2 = Problem.objects.filter(Q(terms__in=termas) | q21 & q22)
            kolvo['podx'] = len(termas2)
            q1 = Q(status='0') & Q(date__range=(date(nowdatetime.year, 1, 1), nowdate))
            q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate)) & Q(status=Status.objects.get(name='В работе'))
            q22 = Q(visible='1') | Q(statussys='1')
            termas = Term.objects.filter(q1)
            termas2 = Problem.objects.filter(Q(terms__in=termas) | q21 & q22)
            kolvo['prosr'] = len(termas2)
        elif request.user.has_perm('problem.user_executor'):
            if userlk.userprofile.org != None:
                userorg = Q(terms__org=userlk.userprofile.org)
            else:
                userorg = Q()
            if userlk.userprofile.dep != None:
                userdep = Q(terms__curat=userlk.userprofile.dep)
                userdep1 = Q(terms__resolutions__curat=userlk.userprofile.dep)
            else:
                userdep = Q()
                userdep1 = Q()
            q1 = Q(visible='1')
            q2 = Q(terms__status='0')
            q3 = userorg | userdep | Q(terms__curatuser=userlk) | userdep1 | Q(terms__resolutions__curatuser=userlk)
            kolvo['kolall'] = len(Problem.objects.filter(q1, q2, q3))
            print(kolvo['kolall'])
            kolvo['kolclose'] = len(Problem.objects.filter(visible='1', statussys='2', terms__answers__user=userlk))
            q1 = Q(status='0')
            q2 = Q(date__range=(nowdate, nowdate+timedelta(3)))
            q31 = Q(org=userlk.userprofile.org) | Q(curat=userlk.userprofile.dep)
            q32 = Q(curatuser=userlk) | Q(resolutions__curat=userlk.userprofile.dep) | Q(resolutions__curatuser=userlk)
            q3 = (q31 | q32)
            termas = Term.objects.filter(q1, q2, q3)
            kolvo['podx'] = len(termas)
            q1 = Q(status='0')
            q2 = Q(date__range=(date(nowdatetime.year, 1, 1), nowdate))
            termas = Term.objects.filter(q1, q2, q3)
            kolvo['prosr'] = len(termas)
        return render(request, 'problem/lk.html', {'kolvo': kolvo})


def closedproblem(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        name = 'Закрытые жалобы'
        userlk = User.objects.get(username=request.user.username)
        otv = Answer.objects.filter(user=userlk)
        prob = []
        for i in otv:
            a = i.otvs.all()
            for j in a:
                c = j.terms.all()
                for h in c:
                    prob.append(h)
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
        if request.user.has_perm('problem.user_supermoderator'):
            if request.method == 'POST':
                formcre = CreateUser(request.POST)
                if formcre.is_valid():
                    passw = ''
                    for i in range(8):
                        passw += random.choice(chars)
                    termp = User.objects.create_user(formcre.cleaned_data.get("username"), formcre.cleaned_data.get("email"), passw)
                    termp.first_name = formcre.cleaned_data.get("first_name")
                    termp.last_name = formcre.cleaned_data.get("last_name")
                    termp.group = Group.objects.get(name=formcre.cleaned_data.get("group"))
                    print(formcre.cleaned_data)
                    if formcre.cleaned_data.get("org"): termp.userprofile__org = Curator.objects.get(name=formcre.cleaned_data.get("org"))
                    if formcre.cleaned_data.get("dep"): termp.userprofile__dep = Department.objects.get(name=formcre.cleaned_data.get("dep").name)
                    mescre = [termp.username, passw]
                    termp.save()
                    return render(request, 'problem/createuser.html', {'formcre': formcre, 'mescre': mescre})
                else:
                    return render(request, 'problem/createuser.html', {'formcre': formcre})
            else:
                formcre = CreateUser()
                return render(request, 'problem/createuser.html', {'formcre': formcre})
        else:
            return redirect('index')

def addparsing(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.has_perm('problem.user_moderator'):
            hist = ActionHistory(act=Action.objects.get(nact='2'), arg=pk, status='0')
            hist.save()
            return redirect("problem", pk=pk)

def dashboard(request):
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
        kolvo['problems'].append(len(Problem.objects.filter(visible='1', dateotv=i)))
    return render(request, 'problem/dashboard.html', {'dates': dates, 'kolvo': kolvo})
