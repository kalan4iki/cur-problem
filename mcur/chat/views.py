from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers

#Project
from problem.models import Problem
from .models import Message

@api_view(['POST'])
def ChatProblem(request):
    zapr = request.POST
    print(zapr)
    if Problem.objects.filter(nomdobr=zapr['nd']).exists():
        prob = Problem.objects.get(nomdobr=zapr['nd'])
        if zapr['action'] == '1':
            mes = prob.chats.all()
            meslist = []
            for i in mes:
                temp = {}
                temp['user'] = f'{i.user.first_name} {i.user.last_name}'
                temp['text'] = f'{i.text}'
                temp['date'] = f'{i.datecre.strftime("%d.%m.%y %H:%M")}'
                meslist.append(temp)
            return JsonResponse({'status': 'successfully', 'mes': meslist})
        elif zapr['action'] == '2':
            user = request.user
            mes = Message(text=zapr['text'], user=user, problem=prob)
            mes.save()
            return JsonResponse({'status': 'successfully'})
        else:
            return JsonResponse({'status': 'error', 'text': 'Invalid action'})
    else:
        return JsonResponse({'status': 'error', 'text': 'Invalid problem'})