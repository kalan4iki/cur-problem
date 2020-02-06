from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.forms import inlineformset_factory, modelform_factory
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from django_tables2.views import MultiTableMixin
from django_tables2.paginators import LazyPaginator
from .models import Problem, Curator, Term, Answer
from .tables import ProblemTable, TermTable
from .forms import PrSet, AuthenticationForm, PrAdd, TermForm
from django.contrib import messages
import random
import mcur.settings as settings

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('__all__')

class ProblemTableView(MultiTableMixin, TemplateView):
    template_name = "problem/test.html"
    table_pagination = {"per_page": 10}
    extra_context= {'curat': Curator.objects.all()}
    def get_tables(self):
        qs = Problem.objects.all()
        return [ProblemTable(qs)]

class CuratorsMenu:
    def __init__(self, curat):
        self.curat = curat

    def codes(self, pk):
        temp = []
        for i in self.curat:
            if i.pk == pk:
                temp.append([i, ' active'])
            elif pk == '-1':
                temp.append([i, ''])
            else:
                temp.append([i, ''])
        return temp

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

def prob(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if Problem.objects.filter(nomdobr=pk).exists():
            prob = Problem.objects.get(nomdobr=pk)
            a = prob.datecrok.all()
            termadd = TermForm()
            return render(request, 'problem/problem.html', {'formadd': termadd, 'np': prob, 'srok': a})
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
                    prob.datecrok.add(a)
                    nd = Problem.objects.get(pk=pk)
                    return redirect("problem", pk=nd.nomdobr)
            else:
                formadd = TermForm()
            return render(request, 'problem/termadd.html', {'auth': True, 'formadd': formadd, 'np': prob, 'prob': prob})
        else:
            return render(request, 'problem/termadd.html', {'auth': False, 'np': prob, 'prob': prob})

def delterm(request, pk, pkp):
    b = Term.objects.get(pk=pk)
    nd = b.terms.all()[0]
    b.delete()
    return redirect("problem", pk=nd.nomdobr)

def lk(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        userlk = User.objects.get(username=request.user.username)
        kolvo = {}
        kolvo['kolclose'] = len(Answer.objects.filter(user=request.user))
        if request.user.has_perm('problem.view_problem'):
            temp = len(Problem.objects.filter(status='Закрыто'))
            kolvo['kolall'] = len(Problem.objects.all()) - temp
        elif userlk.userprofile.org != None:
        #elif request.user.UserProfile.org != None:
            kolvo['kolall'] = (len(Term.objects.filter(curat=userlk.userprofile.org, status='0')) +
                len(Term.objects.filter(curat=userlk.userprofile.org, status='1')))
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

def allproblem(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        name = 'Все жалобы'
        userlk = User.objects.get(username=request.user.username)
        prob = []
        if request.user.has_perm('problem.view_problem'):
            temp = Problem.objects.all()
            for i in temp:
                if i.status != 'Закрыто':
                    prob.append(i)
        else:
            terms = Term.objects.filter(curat=userlk.userprofile.org)
            for i in terms:
                a = i.terms.all()
                for j in a:
                    prob.append(a)
        dop = f'Всего: {len(prob)}.'
        config = RequestConfig(request, paginate={'paginator_class': LazyPaginator, 'per_page': 10})
        table = ProblemTable(prob)
        config.configure(table)
        return render(request, 'problem/allproblem.html', {'table': table, 'name': name, 'dop': dop})

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
