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

class CurLogin(LoginView):
    template_name = 'problem/login.html'
    #authentication_form=AuthenticationForm
    redirect_field_name='next'

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

class ELoginView(View):

    def get(self, request):
        # если пользователь авторизован, то делаем редирект на главную страницу
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        else:
            # Иначе формируем контекст с формой авторизации и отдаём страницу
            # с этим контекстом.
            # работает, как для url - /admin/login/ так и для /accounts/login/
            context = create_context_username_csrf(request)
            return render_to_response('accounts/login.html', context=context)

    def post(self, request):
        # получив запрос на авторизацию
        form = AuthenticationForm(request, data=request.POST)

        # проверяем правильность формы, что есть такой пользователь
        # и он ввёл правильный пароль
        if form.is_valid():
            # в случае успеха авторизуем пользователя
            auth.login(request, form.get_user())
            # получаем предыдущий url
            next = urlparse(get_next_url(request)).path
            # и если пользователь из числа персонала и заходил через url /admin/login/
            # то перенаправляем пользователя в админ панель
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            # иначе делаем редирект на предыдущую страницу,
            # в случае с /accounts/login/ произойдёт ещё один редирект на главную страницу
            # в случае любого другого url, пользователь вернётся на данный url
            return redirect(next)

        # если данные не верны, то пользователь окажется на странице авторизации
        # и увидит сообщение об ошибке
        context = create_context_username_csrf(request)
        context['login_form'] = form

        return render_to_response('accounts/login.html', context=context)


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
    prob = Problem.objects.all()
    curat = Curator.objects.all()
    curats = CuratorsMenu(curat).codes('-1')
    config = RequestConfig(request, paginate={'paginator_class': LazyPaginator, 'per_page': 10})
    table = ProblemTable(prob)
    forms = AuthenticationForm
    config.configure(table)
    return render(request, 'problem/index.html', {'table': table, 'curat': curats, 'loginform': forms})

def curator(request, pk):
    term = Term.objects.filter(curat=Curator.objects.get(pk=pk))
    prob = []
    for i in term:
        prob.append(Problem.objects.get(datecrok=i))
    curat = Curator.objects.all()
    curats = CuratorsMenu(curat).codes(pk)
    config = RequestConfig(request, paginate={'paginator_class': LazyPaginator, 'per_page': 10})
    table = ProblemTable(prob)
    config.configure(table)
    return render(request, 'problem/index.html', {'table': table, 'curat': curats})

def prob(request, pk):
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
    if request.user.is_authenticated:
        a = User.objects.get(username=request.user)
        return render(request, 'problem/lk.html', {'userr': a})
    else:
        return redirect('index')
