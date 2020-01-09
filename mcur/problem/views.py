from django.shortcuts import render
from django_tables2 import RequestConfig
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from .models import Problem, Curator
from .tables import ProblemTable

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

# Create your views here.
def index(request):
    prob = Problem.objects.all()
    curat = Curator.objects.all()
    config = RequestConfig(request)
    table = ProblemTable(prob)
    config.configure(table)
    return render(request, 'problem/index.html', {'table': table, 'curat': curat})

def curator(request, pk):
    prob = Problem.objects.filter(curat=Curator.objects.get(pk=pk))
    curat = Curator.objects.all()
    config = RequestConfig(request)
    table = ProblemTable(prob)
    config.configure(table)
    return render(request, 'problem/index.html', {'table': table, 'curat': curat})

def prob(request, np):
    prob = Problem.objects.get(nomdobr=np)
    return render(request, 'problem/problem.html', {'prob': prob})
