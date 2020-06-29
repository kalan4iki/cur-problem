from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import (Problem, Curator, Term, Answer, Image, Status, Termhistory, Department, Person, Category,
                     UserProfile, Minis, Author)
from parsers.models import ActionHistory, Action, Parser

# other
from datetime import date, timedelta, datetime
from sys import platform
from operator import itemgetter
import xlwt
import random
import os
import logging
import traceback

logger_error = logging.getLogger('file_error')


class Messages(object):
    def __init__(self, *args, **kwargs):
        self.request = dict()
        self.content = dict()
        self.title = ''
        self.mes = ''
        self.status = 0
        self.other = dict()
        self.actionlist = dict()

    def __return__(self):
        context = {
            'title': self.title,
            'message': self.mes,
            'status': self.status,
            'content': self.content
        }
        return JsonResponse(context)

    def __call__(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs['request']
            if self.request.method == 'POST':
                if 'action' in self.request.POST:
                    action = f"action_{self.request.POST['action']}"
                    if action in self.actionlist:
                        temp = self.actionlist[action]
                    else:
                        self.mes = 'Данное действие не существует'
                        self.status = 4
                else:
                    self.mes = 'Ошибка формирования запроса'
                    self.status = 3
            else:
                self.mes = 'Неправильный метод запроса'
                self.status = 2
        else:
            self.mes = 'Ошибка формирования запроса'
            self.status = 1
        self.__return__()


class dashboard(Messages):
    def __init__(self):
        super().__init__()
        self.title = 'Загрузка графика'
        self.mes = 'График загружен'
        self.status = 0
        self.content = {}
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        self.other['nowdate'] = nowdate
        self.actionlist = {
            'action_1': self.action_1,
            'action_2': self.action_2,
            'action_3': self.action_3,
            'action_4': self.action_4,
            'action_5': self.action_5,
            'action_6': self.action_6,
            'action_7': self.action_7,
        }

    def action_1(self):
        self.content['subobjects'] = []
        for i in range(6, 0, -1):
            self.content['subobjects'].append(self.other['nowdate'] - timedelta(i))
        self.content['subobjects'].append(self.other['nowdate'])
        self.content['objects'] = []
        for i in self.content['subobjects']:
            self.content['objects'].append(len(Term.objects.filter(datecre=i)))

    def action_2(self):
        self.content['subobjects'] = []
        for i in range(0, 7):
            self.content['subobjects'].append(self.other['nowdate'] + timedelta(i))
        self.content['objects'] = []
        for i in self.content['subobjects']:
            q1 = Q(status='0') & Q(date=i)
            q21 = Q(dateotv=i)
            q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
                status__in=Status.objects.filter(name='Указан срок')))
            termas = Term.objects.filter(q1)
            termas2 = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
            self.content['objects'].append(len(termas2))

    def action_3(self):
        temporg = Curator.objects.all().exclude(name='Территориальное управление')
        self.content['subobjects'] = []
        self.content['objects'] = []
        for i in temporg:
            self.content['subobjects'].append(i.name)
            self.content['objects'].append(len(Term.objects.filter((Q(org=i) | Q(curat__org=i)) &
                                                                   Q(problem__visible='1'))))

    def action_4(self):
        tempty = Minis.objects.all()
        self.content['subobjects'] = []
        self.content['objects'] = []
        for i in tempty:
            self.content['subobjects'].append(i.name)
            te = len(Problem.objects.filter(Q(ciogv=i) & Q(visible='1')))
            self.content['objects'].append(te)

    def action_5(self):
        self.content['subobjects'] = ''
        author = Author.objects.all()
        temp = {}
        self.content['objects'] = []
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
            self.content['objects'].append(a)

    def action_6(self):
        self.content['subobjects'] = []
        for i in range(6, 0, -1):
            self.content['subobjects'].append(self.other['nowdate'] - timedelta(i))
        self.content['subobjects'].append(self.other['nowdate'])
        self.content['objects'] = []
        for i in self.content['subobjects']:
            self.content['objects'].append(len(Problem.objects.filter(datecre=i)))

    def action_7(self):
        cats = Category.objects.all()
        self.content['objects'] = []
        self.content['subobjects'] = []
        self.content['notes'] = []
        for i in range(4, 0, -1):
            temp = self.other['nowdate'] - timedelta(i)
            self.content['subobjects'].append(temp)
            self.content['notes'].append(temp.strftime('%d.%m.%Y'))
        self.content['subobjects'].append(self.other['nowdate'])
        self.content['notes'].append(self.other['nowdate'].strftime('%d.%m.%Y'))
        temp = {}
        for j in cats:
            temp[j.pk] = len(Problem.objects.filter(temat=j, datecre__range=[self.other['nowdate'][0],
                                                                             self.other['nowdate'][-1]]))
        temp = sorted(temp.items(), key=itemgetter(1), reverse=True)
        for i in range(5):
            nom = temp[i][0]
            cat = Category.objects.get(pk=nom)
            a = {'nam': cat.name}
            c = 1
            for j in self.content['subobjects']:
                a[f'd{c}'] = len(Problem.objects.filter(temat=cat, datecre=j))
                c += 1
            self.content['objects'].append(a)


ns = {
    'message': Messages,
    'dashboard': dashboard
}


def api_func(func):
    try:
        fun = ns[func.lower()]
    except:
        logger_error.error(traceback.format_exc())
    return fun