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
from .forms import (PrAdd, TermForm, AnswerForm,ResolutionForm, CreateUser, TyForm)
from .logick import lk_dispatcher, lk_executor, lk_moderator, lk_ty
from mcur import settings

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
        self.context = dict()
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        self.other['nowdatetime'] = nowdatetime
        self.other['nowdate'] = nowdate

    def __return__(self):
        self.context = {
            'title': self.title,
            'message': self.mes,
            'status': self.status,
            'content': self.content
        }

    def __call__(self, *args, **kwargs):
        debugs = ''
        if "request" in kwargs:
            self.request = kwargs['request']
            if self.request.method == 'POST':
                if 'action' in self.request.POST:
                    action = f"action_{self.request.POST['action']}"
                    if action in self.actionlist:
                        self.content['action'] = self.request.POST['action']
                        temp = self.actionlist[action]()
                    else:
                        self.mes = 'Данное действие не существует'
                        self.status = 4
                        debugs = f'Ошибка номер: {self.status}'
                else:
                    self.mes = 'Ошибка формирования запроса'
                    self.status = 3
                    debugs = f'Ошибка номер: {self.status}'
            else:
                self.mes = 'Неправильный метод запроса'
                self.status = 2
                debugs = f'Ошибка номер: {self.status}'
        else:
            self.mes = 'Ошибка формирования запроса'
            self.status = 1
            debugs = f'Ошибка номер: {self.status}'
        self.__return__()


class dashboard(Messages):
    '''Страница "Статистика и отчетность"'''
    def __init__(self):
        super().__init__()
        self.title = 'Загрузка графика'
        self.mes = 'График загружен'
        self.actionlist = {
            'action_1': self.action_1,
            'action_2': self.action_2,
            'action_3': self.action_3,
            'action_4': self.action_4,
            'action_5': self.action_5,
            'action_6': self.action_6,
            'action_7': self.action_7,
            'action_8': self.action_8,
            'action_9': self.action_9,
            'action_10': self.action_10,
            'action_11': self.action_11,
        }

    def action_1(self):
        '''График "Назначения"'''
        self.content['subobjects'] = []
        for i in range(6, 0, -1):
            self.content['subobjects'].append(self.other['nowdate'] - timedelta(i))
        self.content['subobjects'].append(self.other['nowdate'])
        self.content['objects'] = []
        for i in self.content['subobjects']:
            self.content['objects'].append(len(Term.objects.filter(datecre=i)))

    def action_2(self):
        '''График "Обращения"'''
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
        '''График "Статистика организаций"'''
        temporg = Curator.objects.all().exclude(name='Территориальное управление')
        self.content['subobjects'] = []
        self.content['objects'] = []
        for i in temporg:
            self.content['subobjects'].append(i.name)
            self.content['objects'].append(len(Term.objects.filter((Q(org=i) | Q(curat__org=i)) &
                                                                   Q(problem__visible='1'))))

    def action_4(self):
        '''График "Статистика ТУ"'''
        tempty = Minis.objects.all()
        self.content['subobjects'] = []
        self.content['objects'] = []
        for i in tempty:
            self.content['subobjects'].append(i.name)
            te = len(Problem.objects.filter(Q(ciogv=i) & Q(visible='1')))
            self.content['objects'].append(te)

    def action_5(self):
        '''График "Топ 25 авторов"'''
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
        '''График "Новые обращения"'''
        self.content['subobjects'] = []
        for i in range(6, 0, -1):
            self.content['subobjects'].append(self.other['nowdate'] - timedelta(i))
        self.content['subobjects'].append(self.other['nowdate'])
        self.content['objects'] = []
        for i in self.content['subobjects']:
            self.content['objects'].append(len(Problem.objects.filter(datecre=i)))

    def action_7(self):
        '''График "Топ 5 категорий за период"'''
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
            temp[j.pk] = len(Problem.objects.filter(temat=j, datecre__range=[self.content['subobjects'][0],
                                                                             self.content['subobjects'][-1]]))
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

    def action_8(self):
        '''Отчет "за определенный период"'''
        if 'linux' in platform.lower():
            temp = self.request.POST['datefrom'].split('-')
            datefrom = date(int(temp[0]), int(temp[1]), int(temp[2]))
            temp = self.request.POST['datebefore'].split('-')
            datebefore = date(int(temp[0]), int(temp[1]), int(temp[2]))
        else:
            datefrom = date.fromisoformat(self.request.POST['datefrom'])
            datebefore = date.fromisoformat(self.request.POST['datebefore'])
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('problems')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес',
                   'Дата жалобы',
                   'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе', 'Тер управление']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = Problem.objects.filter(datecre__range=(datefrom, datebefore)).values_list('pk', 'nomdobr',
                                                'temat__name', 'podcat__name', 'text', 'adres', 'datecre',
                                                 'dateotv', 'status__name', 'statussys', 'ciogv__name')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                if col_num == 6 or col_num == 7:
                    ws.write(row_num, col_num, f'{row[col_num].day}.{row[col_num].month}.{row[col_num].year}',
                             font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)
        name = f'act{self.content["action"]}-{self.other["nowdatetime"].strftime("%d%m%Y%H%M%S")}.xls'
        wb.save(f'{settings.MEDIA_ROOT}xls/{name}')
        if 'linux' in platform.lower():
            url = f'https://skiog.ru/media/xls/{name}'
        else:
            url = f'http://127.0.0.1:8000/media/xls/{name}'
        self.title = 'Подготовка отчета'
        self.mes = 'Отчет "за определенный период" готов'
        self.content['url'] = url

    def action_9(self):
        '''Отчет "не закрытые обращения"'''
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('problems')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес',
                   'Дата жалобы',
                   'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе', 'Тер управление']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = Problem.objects.filter(visible='1').values_list('pk', 'nomdobr', 'temat__name', 'podcat__name',
                                                 'text', 'adres', 'datecre',
                                                 'dateotv', 'status__name', 'statussys', 'ciogv__name')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                if col_num == 6 or col_num == 7:
                    ws.write(row_num, col_num, f'{row[col_num].day}.{row[col_num].month}.{row[col_num].year}',
                             font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)
        name = f'act{self.content["action"]}-{self.other["nowdatetime"].strftime("%d%m%Y%H%M%S")}.xls'
        wb.save(f'{settings.MEDIA_ROOT}xls/{name}')
        if 'linux' in platform.lower():
            url = f'https://skiog.ru/media/xls/{name}'
        else:
            url = f'http://127.0.0.1:8000/media/xls/{name}'
        self.title = 'Подготовка отчета'
        self.mes = 'Отчет "не закрытые обращения" готов'
        self.content['url'] = url

    def action_10(self):
        '''Отчет "статистика по категориям"'''
        if 'linux' in platform.lower():
            temp = self.request.POST['datefrom'].split('-')
            datefrom = date(int(temp[0]), int(temp[1]), int(temp[2]))
            temp = self.request.POST['datebefore'].split('-')
            datebefore = date(int(temp[0]), int(temp[1]), int(temp[2]))
        else:
            datefrom = date.fromisoformat(self.request.POST['datefrom'])
            datebefore = date.fromisoformat(self.request.POST['datebefore'])
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('problems')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.alignment.horz = 0x02
        cats = Category.objects.all()
        tempdate = []
        notes = []
        days = datebefore - datefrom
        tempdate.append(datefrom)
        notes.append('Наименование')
        notes.append(datefrom.strftime('%d.%m.%Y'))
        first_col = ws.col(0)
        first_col.width = 256 * 20
        for i in range(days.days):
            td = tempdate[-1] + timedelta(1)
            tempdate.append(td)
            notes.append(td.strftime('%d.%m.%Y'))
            col = ws.col(i+1)
            col.width = 256 * 10
        col = ws.col(days.days+1)
        col.width = 256 * 10
        col = ws.col(days.days + 2)
        col.width = 256 * 10
        notes.append('Итого')
        temp = []
        for i in cats:
            c = []
            d = 0
            c.append(i.name)
            for j in tempdate:
                ea = len(Problem.objects.filter(temat=i, datecre=j))
                d += ea
                c.append(ea)
            c.append(d)
            temp.append(c)
        columns = notes
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        temp = sorted(temp, key=itemgetter(days.days+2), reverse=True)
        rows = temp
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        name = f'act{self.content["action"]}-{self.other["nowdatetime"].strftime("%d%m%Y%H%M%S")}.xls'
        wb.save(f'{settings.MEDIA_ROOT}xls/{name}')
        if 'linux' in platform.lower():
            url = f'https://skiog.ru/media/xls/{name}'
        else:
            url = f'http://127.0.0.1:8000/media/xls/{name}'
        self.title = 'Подготовка отчета'
        self.mes = 'Отчет "статистика по категориям" готов'
        self.content['url'] = url

    def action_11(self):
        '''Отчет "выгрузка по автору"'''
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('problems')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['№ п/п', 'Номер в доброделе', 'Тематика', 'Категория', 'Текст обращения', 'Адрес',
                   'Дата жалобы',
                   'Дата ответа по доброделу', 'Статус в доброделе', 'Статус в системе', 'Тер управление']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        author = Author.objects.get(pk=int(self.request.POST['pk']))
        rows = Problem.objects.filter(author=author).values_list('pk', 'nomdobr', 'temat__name', 'podcat__name',
                                                 'text', 'adres', 'datecre',
                                                 'dateotv', 'status__name', 'statussys', 'ciogv__name')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                if col_num == 6 or col_num == 7:
                    ws.write(row_num, col_num, f'{row[col_num].day}.{row[col_num].month}.{row[col_num].year}',
                             font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)
        name = f'act{self.content["action"]}-{self.other["nowdatetime"].strftime("%d%m%Y%H%M%S")}.xls'
        wb.save(f'{settings.MEDIA_ROOT}xls/{name}')
        if 'linux' in platform.lower():
            url = f'https://skiog.ru/media/xls/{name}'
        else:
            url = f'http://127.0.0.1:8000/media/xls/{name}'
        self.title = 'Подготовка отчета'
        self.mes = 'Отчет "выгрузка по автору" готов'
        self.content['url'] = url


class problem(Messages):
    '''Страница "Проблема"'''
    def __init__(self):
        super().__init__()
        self.status = 0
        self.actionlist = {
            'action_1': self.action_1,
            'action_2': self.action_2,
            'action_3': self.action_3,
            'action_4': self.action_4,
            'action_5': self.action_5,
            'action_6': self.action_6,
            'action_7': self.action_7,
            'action_8': self.action_8,
        }

    def action_1(self):
        '''Операция "отправить на обновление"'''
        pk = self.request.POST['pk']
        self.title = 'Обновление обращения'
        self.mes = f'Обращение №{pk} отправлено на обновление'
        hist = ActionHistory(act=Action.objects.get(nact='2'), arg=pk, status='0')
        hist.save()

    def action_2(self):
        '''Операция "отображение назначений" не нужная функция'''
        pass

    def action_3(self):
        '''Операция "удаление назначения"'''
        pk = self.request.POST['pk']
        self.title = 'Удаление назначения'
        self.mes = 'Назначение удалено'
        b = Term.objects.get(pk=pk)
        nd = b.problem
        b.delete()
        if len(nd.terms.all()) == 0:
            nd.statussys = '2'
            nd.save()

    def action_4(self):
        '''Операция "утверждение назначений"'''
        self.title = 'Утверждение назначений'
        self.mes = 'Назначение утверждено.'
        pk = self.request.POST['pk']
        term = Term.objects.get(pk=pk)
        term.status = '2'
        term.save()


    def action_5(self):
        '''Операция "изменение назначения"'''
        if 'view' in self.request.POST:
            term = Term.objects.get(pk=self.request.POST['pk'])
            self.content['date'] = term.date.strftime('%Y-%m-%d')
        elif 'change' in self.request.POST:
            self.title = 'Изменение назначения'
            self.mes = 'Изменение успешно.'
            term = Term.objects.get(pk=self.request.POST['pk'])
            ndate = self.request.POST['date'].split('-')
            term.date = date(int(ndate[0]), int(ndate[1]), int(ndate[2]))
            term.save()

    def action_6(self):
        '''Операция "назначение ТУ"'''
        self.title = 'Назначение ТУ'
        self.mes = 'Успешно, территориальное управление добавлено.'
        proble = Problem.objects.get(nomdobr=self.request.POST['pk'])
        proble.ciogv = Minis.objects.get(pk=self.request.POST['name'])
        proble.save()

    def action_7(self):
        '''Операция "подготовка pdf"'''
        pass

    def action_8(self):
        '''Операция "добавление назначения"'''
        self.title = 'Добавление назначения'
        self.mes = 'Назначение успешно добавлено.'
        formadd = TermForm(self.request.POST)
        pk = self.request.POST['pk']
        if formadd.is_valid():
            a = formadd.save()
            nd = Problem.objects.get(nomdobr=pk)
            a.problem = nd
            a.user = self.request.user
            if a.further == False:
                a.furtherdate = None
            a.save()
            nd.statussys = '1'
            nd.save()
            if a.curatuser:
                temp = f'{a.date.day}.{a.date.month}.{a.date.year}'
                #Mailsend(a.curatuser.email, temp, a.problem.nomdobr)


class analysis(Messages):
    '''Страница "Проблема"'''
    def __init__(self):
        super().__init__()
        self.status = 0
        self.actionlist = {
            'action_1': self.action_1,
        }

    def action_1(self):
        pass


ns = {
    'message': Messages,
    'dashboard': dashboard,
    'problem': problem,
    'analysis': analysis,
}


def api_func(func):
    try:
        fun = ns[func.lower()]
    except:
        logger_error.error(traceback.format_exc())
    return fun
