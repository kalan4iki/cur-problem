from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django_tables2 import RequestConfig
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView
from django.forms import inlineformset_factory, modelform_factory
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from django_tables2.views import MultiTableMixin
from django_tables2.paginators import LazyPaginator
from .models import Problem, Curator, Term, Answer, Image, Status
from .tables import ProblemTable, TermTable
from .forms import PrSet, AuthenticationForm, PrAdd, TermForm, AnswerForm
from .filter import ProblemListView, ProblemFilter
from datetime import date, timedelta, datetime
from django.contrib import messages
import random
import xlwt
import mcur.settings as settings

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('__all__')

@api_view(['GET'])
def api_problem(request):
    if request.method == 'GET':
        prob = Problem.objects.all()
        serializer = ProblemSerializer(prob, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def api_problem_detail(request, np):
    if request.method == 'GET':
        prob = Problem.objects.get(nomdobr=np)
        serializer = ProblemSerializer(prob)
        return Response(serializer.data)

class ProblemListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "problem/allproblem.html"
    filterset_class = ProblemFilter

    def get_context_data(self, **kwargs):
        context = super(ProblemListView, self).get_context_data(**kwargs)
        #a = self.object_list
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            prob = Problem.objects.filter(visible='1')
            userlk = User.objects.get(username=self.request.user.username)
            if not self.request.user.has_perm('problem.view_problem'):
                terms = Term.objects.filter(curat=userlk.userprofile.org)
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
        #a = self.object_list
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            prob = Problem.objects.filter(visible='1', statussys='2')
            userlk = User.objects.get(username=self.request.user.username)
            if not self.request.user.has_perm('problem.view_problem'):
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
        #a = self.object_list
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            nowdatetime = datetime.now()
            nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
            if not self.request.user.has_perm('problem.view_problem'):
                terms = Term.objects.filter(status='0', curat=userlk.userprofile.org, date__range=(nowdate, nowdate + timedelta(3)))
                prob = Problem.objects.filter(terms__in=terms, visible='1', statussys='1')
            else:
                terms = Term.objects.filter(status='0', date__range=(nowdate, nowdate + timedelta(3)))
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
        #a = self.object_list
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            userlk = User.objects.get(username=self.request.user.username)
            nowdatetime = datetime.now()
            nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
            if not self.request.user.has_perm('problem.view_problem'):
                terms = Term.objects.filter(status='0', curat=userlk.userprofile.org, date__range=(date(nowdatetime.year, 1, 1), nowdate))
                prob = Problem.objects.filter(terms__in=terms, visible='1', statussys='1')
            else:
                terms = Term.objects.filter(status='0', date__range=(date(nowdatetime.year, 1, 1), nowdate))
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

def proverka(request, term):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if not request.user.has_perm(''):
            return redirect('index')

def Answer_approve(request, pk):
    term = 'problem.change_answer'
    proverka(request, term)
    anw = Answer.objects.get(pk=pk)
    anw.status = '1'
    anw.term.status = '2'
    anw.term.anwr = True
    anw.save()
    anw.term.save()
    return redirect('termview',pk=anw.term.pk)

def Answer_modify(request, pk):
    term = 'problem.change_answer'
    proverka(request, term)
    anw = Answer.objects.get(pk=pk)
    anw.status = '2'
    anw.term.status = '0'
    anw.term.anwr = False
    anw.save()
    anw.term.save()
    return redirect('termview',pk=anw.term.pk)

def prob(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if Problem.objects.filter(nomdobr=pk).exists():
            prob = Problem.objects.get(nomdobr=pk)
            a = Term.objects.filter(problem=prob)
            userr = User.objects.get(username=request.user.username)
            c = False
            for i in a:
                if i.curat == userr.userprofile.org:
                    c = True
            if request.user.has_perm('problem.view_problem'):
                c = True
            if c:
                termadd = TermForm()
                answeradd = AnswerForm()
                return render(request, 'problem/problem.html', {'answeradd': answeradd, 'formadd': termadd, 'np': prob, 'srok': a})
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
                    #if not Problem.objects.filter(nomdobr=request.POST['nomdobr']).exists():
                    #    messages.error(request, 'Данная жалоба существует.')
                    #    return redirect("problem", pk= Problem.objects.get(nomdobr=request.POST['nomdobr']).pk)
                    return redirect("index")
            else:
                return redirect("problem", pk=Problem.objects.get(nomdobr=request.POST['nomdobr']).pk)

def termadd(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        prob = Problem.objects.get(pk=pk)
        if request.user.has_perm('problem.edit_Problem'):
            if request.method == 'POST':
                formadd = TermForm(request.POST)
                if formadd.is_valid():
                    a = formadd.save()
                    nd = Problem.objects.get(pk=pk)
                    a.problem = nd
                    a.save()
                    nd.statussys = '1'
                    nd.save()
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
        if request.user.has_perm('problem.view_problem'):
            kolvo['kolall'] = len(Problem.objects.filter(visible='1'))
            kolvo['kolno'] = len(Problem.objects.filter(visible='1', statussys='2'))
            termas = Term.objects.filter(status='0', date__range=(nowdate, nowdate+timedelta(3)))
            kolvo['podx'] = len(termas)
            termas = Term.objects.filter(status='0', date__range=(date(nowdatetime.year, 1, 1), nowdate))
            kolvo['prosr'] = len(termas)
        elif userlk.userprofile.org != None:
            kolvo['kolclose'] = len(Answer.objects.filter(user=request.user))
            termas = Term.objects.filter(status='0', curat=Curator.objects.get(name=userlk.userprofile.org), date__range=(nowdate, nowdate+timedelta(3)))
            kolvo['podx'] = len(termas)
            termas = Term.objects.filter(status='0', curat=Curator.objects.get(name=userlk.userprofile.org), date__range=(date(nowdatetime.year, 1, 1), nowdate))
            kolvo['prosr'] = len(termas)
            kolvo['kolall'] = len(Term.objects.filter(curat=userlk.userprofile.org).distinct())
        return render(request, 'problem/lk.html', {'kolvo': kolvo})

def closedproblem(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        name = 'Закрытые жалобы'
        userlk = User.objects.get(username=request.user.username)
        otv = Answer.objects.filter(user=userlk)
        #terms = Term.objects.filter(curat=userlk.userprofile.org)
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

def termview(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if Term.objects.filter(pk=pk).exists():
            terr = Term.objects.get(pk=pk)
            answ = []
            try:
                answ = terr.answers.all()
            except ObjectDoesNotExist:
                answ = []
            print(answ)
            userr = User.objects.get(username=request.user.username)
            c = False
            if terr.curat == userr.userprofile.org:
                c = True
            if request.user.has_perm('problem.view_term'):
                c = True
            print(answ)
            if c:
                answeradd = AnswerForm()
                return render(request, 'problem/term.html', {'term': terr, 'answers': answ, 'answeradd': answeradd})
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

    columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес', 'Дата жалобы', 'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Problem.objects.all().values_list('pk', 'nomdobr', 'temat__name', 'podcat__name', 'text', 'adres', 'datecre', 'dateotv', 'status', 'statussys')
    for row in rows:

        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def custom404(request):
    render(request, 'problem/404.html')
