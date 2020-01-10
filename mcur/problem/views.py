from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.forms import inlineformset_factory, modelform_factory
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from django_tables2.views import MultiTableMixin
from django_tables2.paginators import LazyPaginator
from .models import Problem, Curator
from .tables import ProblemTable
from .forms import PrSet
import random

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
    prob = Problem.objects.all()
    curat = Curator.objects.all()
    curats = CuratorsMenu(curat).codes('-1')
    config = RequestConfig(request, paginate={'paginator_class': LazyPaginator, 'per_page': 10})
    table = ProblemTable(prob)
    config.configure(table)
    return render(request, 'problem/index.html', {'table': table, 'curat': curats})

def curator(request, pk):
    prob = Problem.objects.filter(curat=Curator.objects.get(pk=pk))
    curat = Curator.objects.all()
    curats = CuratorsMenu(curat).codes(pk)
    config = RequestConfig(request, paginate={'paginator_class': LazyPaginator, 'per_page': 10})
    table = ProblemTable(prob)
    config.configure(table)
    return render(request, 'problem/index.html', {'table': table, 'curat': curats})

def prob(request, pk):
    prob = Problem.objects.get(pk=pk)
#    PrForm = modelform_factory(Problem, fields={'temat', 'ciogv', 'curat', 'text', 'adres', 'status', 'datecre', 'datecrok', 'dateotv'})
    if request.method == 'POST':
        formset = PrSet(request.POST, instance=prob)
        if formset.is_valid():
            formset.save()
            return redirect("index")
    else:
        formset = PrSet(instance=prob)
    return render(request, 'problem/problem.html', {'formset': formset, 'np': prob.nomdobr})

def zaptable(request):
    for i in range(0,51):
        temp = random.randint(3000000,4000000)
        a = Problem()
        a.nomdobr = temp
        a.save()
