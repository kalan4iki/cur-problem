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
from .models import Problem, Curator, Term
from .tables import ProblemTable, TermTable
from .forms import PrSet, AuthenticationForm, PrAdd, TermForm
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

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        prob = Problem.objects.all()
        curat = Curator.objects.all()
        curats = CuratorsMenu(curat).codes('-1')
        config = RequestConfig(request, paginate={'paginator_class': LazyPaginator, 'per_page': 10})
        table = ProblemTable(prob)
        forms = AuthenticationForm
        config.configure(table)
        return render(request, 'problem/index.html', {'table': table, 'curat': curats, 'loginform': forms})

def curator(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        term = Term.objects.filter(curat=Curator.objects.get(pk=pk))
        prob = []
        for i in term:
            prob.append(Term.objects.filter(problem__pk=i.pk))
            #prob.append(Problem.objects.get(datecrok=i))
        curat = Curator.objects.all()
        curats = CuratorsMenu(curat).codes(pk)
        config = RequestConfig(request, paginate={'paginator_class': LazyPaginator, 'per_page': 10})
        table = ProblemTable(prob)
        config.configure(table)
        return render(request, 'problem/index.html', {'table': table, 'curat': curats})

def prob(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        prob = Problem.objects.get(pk=pk)
        a = prob.datecrok.all()
        if request.user.has_perm('problem.edit_Problem'):
            if request.method == 'POST':
                formset = PrSet(request.POST, instance=prob)
                if formset.is_valid():
                    formset.save()
                    return redirect("index")
            else:
                formset = PrSet(instance=prob)
            return render(request, 'problem/problem.html', {'auth': True, 'formset': formset, 'np': prob, 'prob': prob, 'srok': a})
        else:
            return render(request, 'problem/problem.html', {'auth': False, 'np': prob, 'prob': prob, 'srok': a})

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
            if request.method == 'POST':
                formadd = PrAdd(request.POST)
                if formadd.is_valid():
                    formadd.save()
                    return redirect("problem", pk= Problem.objects.get(nomdobr=request.POST['nomdobr']).pk)
                else:
                    return redirect("index")
            else:
                return redirect("index")

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
                    print(a)
                    prob.datecrok.add(a)
                    return redirect("problem", pk=pk)
            else:
                formadd = TermForm()
            return render(request, 'problem/termadd.html', {'auth': True, 'formadd': formadd, 'np': prob, 'prob': prob})
        else:
            return render(request, 'problem/termadd.html', {'auth': False, 'np': prob, 'prob': prob})

def delterm(request, pk, pkp):
    b = Term.objects.get(pk=pk)
    b.delete()
    return redirect("problem", pk=pkp)

def lk(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        a = User.objects.get(username=request.user)
        return render(request, 'problem/lk.html', {'userr': a})
