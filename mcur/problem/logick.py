from .models import (Problem, Term, Answer, Status, Termhistory)
from django.contrib import messages
from django.db.models import Q
from datetime import date, timedelta, datetime


class lk_objects(object):
    def __init__(self, *args, **kwargs):
        self.actionlist = dict()
        self.request = dict()
        self.prob = list()
        self.box = ''
        self.action = ''

    def __call__(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs['request']
            if self.request.method == 'POST':
                self.box = self.request.POST['action']
                self.actionlist[self.request.POST['action'].lower()]()
            elif self.request.method == 'GET':
                self.action = kwargs['action']
                self.actionlist[self.action.lower()]()
        else:
            messages.error(self.request, 'Неправильный запрос.')
            return redirect('index')


# Область исполнителя
class lk_executor(lk_objects):
    def __init__(self):
        super().__init__()
        self.actionlist = {
            'closed': self.b1,
            'allproblem': self.b2,
            'podxproblem': self.b3,
            'todayproblem': self.b4,
            'prosrproblem': self.b5,
            'meproblem': self.b6
        }

    def b1(self): # Ответы
        userlk = self.request.user
        q1 = Q(user=userlk)
        termas = Answer.objects.filter(q1)
        termas2 = Term.objects.filter(answers__in=termas)
        self.prob = Problem.objects.filter(visible='1', terms__in=termas2)

    def b2(self): # Все обращения
        userlk = self.request.user
        if userlk.userprofile.dep == None:
            q1 = Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
        else:
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
        termas2 = Term.objects.filter((q1 | Q(resolutions__in=termas)) & (Q(status='0') | Q(status='1')))
        self.prob = Problem.objects.filter((Q(visible='1') & Q(statussys='1')) & Q(terms__in=termas2))

    def b3(self): # Подходит срок
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        if userlk.userprofile.dep == None:
            q1 = Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
        else:
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
        q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
        q2 = Q(visible='1')
        q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        self.prob = Problem.objects.filter(Q(terms__in=termas1) & q21 & q2)

    def b4(self): # Обращения на сегодня
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        if userlk.userprofile.dep == None:
            q1 = Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
        else:
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
        q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
        q2 = Q(visible='1')
        q21 = Q(dateotv=nowdate)
        self.prob = Problem.objects.filter((Q(terms__in=termas1) & q21) & q2)

    def b5(self): # Просроченные
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        if userlk.userprofile.dep == None:
            q1 = Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
        else:
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
        q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(date(2019, 1, 1), nowdate - timedelta(1)))
        termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
        q2 = Q(visible='1') & Q(statussys='1')
        q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
        self.prob = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)

    def b6(self): # Мои обращения
        userlk = self.request.user
        q1 = Q(curatuser=userlk)
        termas = Term.objects.filter(q1)
        self.prob = Problem.objects.filter(Q(terms__in=termas) & Q(visible='1'))


# Область диспетчера
class lk_dispatcher(lk_objects):
    def __init__(self):
        super().__init__()
        self.actionlist = {
            'allproblem': self.b1,
            'closed': self.b2,
            'podxproblem': self.b3,
            'todayproblem': self.b4,
            'prosrproblem': self.b5
        }

    def b1(self): #Все обращения
        userlk = self.request.user
        org = userlk.userprofile.org
        q1 = Q(curatuser=userlk)
        termas = Termhistory.objects.filter(q1)
        q1 = (Q(org=org) | Q(curat__org=org) | Q(curatuser=userlk))
        termas2 = Term.objects.filter((q1 | Q(resolutions__in=termas)) & (Q(status='0') | Q(status='1')))
        self.prob = Problem.objects.filter(Q(visible='1') & Q(terms__in=termas2))


    def b2(self): #Ответы
        userlk = self.request.user
        q1 = Q(user=userlk)
        termas = Answer.objects.filter(q1)
        termas2 = Term.objects.filter(answers__in=termas)
        self.prob = Problem.objects.filter(visible='1', terms__in=termas2)

    def b3(self): #Подходит срок
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        # Проверка резолюций
        q1 = Q(terms__resolutions__curatuser=userlk)
        # Проверка направлений
        q2 = (Q(terms__org=userlk.userprofile.org) | Q(terms__curat__org=userlk.userprofile.org) | Q(terms__curatuser=userlk))
        q3 = (Q(terms__status__in=['0', '1']) & Q(terms__date__range=(nowdate + timedelta(1), nowdate + timedelta(4))))
        # Проверка обращений
        q4 = Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        q5 = Q(visible='1') & Q(statussys='1')
        self.prob = Problem.objects.filter((q1 | (q2 & q3) | q4) & q5)

    def b4(self): #Обращения на сегодня
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        #Проверка резолюций
        q1 = Q(terms__resolutions__curatuser=userlk)
        #Проверка направлений
        q2 = (Q(terms__org=userlk.userprofile.org) | Q(terms__curat__org=userlk.userprofile.org) | Q(terms__curatuser=userlk))
        q3 = Q(terms__status__in=['0', '1']) & Q(terms__date=nowdate)
        #Проверка обращений
        q4 = Q(dateotv=nowdate)
        q5 = Q(visible='1') & Q(statussys='1')
        self.prob = Problem.objects.filter((q1 | (q2 & q3) | q4) & q5)

    def b5(self): #Просроченные
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        q1 = Q(curatuser=userlk)
        termas = Termhistory.objects.filter(q1)
        q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk) | Q(curat__org=userlk.userprofile.org)
        q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(date(2019, 1, 1), nowdate - timedelta(1)))
        termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
        q2 = Q(visible='1') & Q(statussys='1')
        q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
        self.prob = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)

# Область модератора
class lk_moderator(lk_objects):
    def __init__(self):
        super().__init__()
        self.actionlist = {
            'closed': self.b1,
            'noproblem': self.b2,
            'allproblem': self.b3,
            'meproblem': self.b4,
            'podxproblem': self.b5,
            'todayproblem': self.b6,
            'prosrproblem': self.b7,
            'typroblem': self.b8,
            'fuproblem': self.b9
        }

    def b1(self): #Ответы
        userlk = self.request.user
        self.prob = Problem.objects.filter(visible='1', statussys='2', terms__answers__user=userlk)

    def b2(self): #Не распределенные
        userlk = self.request.user
        #prob = Problem.objects.filter(visible='1', statussys='2')
        self.prob = Problem.objects.filter(Q(visible='1') & Q(terms=None))

    def b3(self): # Все обращения
        userlk = self.request.user
        self.prob = Problem.objects.filter(visible='1')

    def b4(self): # Мои обращения
        userlk = self.request.user
        q1 = Q(curatuser=userlk)
        termas = Term.objects.filter(q1)
        self.prob = Problem.objects.filter(Q(terms__in=termas) & Q(visible='1'))

    def b5(self): # Подходит срок
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        q1 = (Q(status='0') | Q(status='1')) & Q(date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
            status__in=Status.objects.filter(name='Указан срок')))
        termas = Term.objects.filter(q1)
        self.prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)

    def b6(self): # Обращения на сегодня
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        q1 = (Q(status='0') | Q(status='1')) & Q(date=nowdate)
        q21 = Q(dateotv=nowdate)
        q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
            status__in=Status.objects.filter(name='Указан срок')))
        termas = Term.objects.filter(q1)
        self.prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)

    def b7(self): # Просроченные
        userlk = self.request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        q1 = (Q(status='0') | Q(status='1')) & Q(
            date__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
        q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
        q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
            status__in=Status.objects.filter(name='Указан срок')))
        termas = Term.objects.filter(q1)
        self.prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)

    def b8(self): # ТУ лист
        userlk = self.request.user
        self.prob = Problem.objects.filter(Q(ciogv=None) & Q(visible='1'))

    def b9(self): # Обещанные
        userlk = self.request.user
        term = Term.objects.filter(further=True).order_by('furtherdate')
        self.prob = Problem.objects.filter(terms__in=term)


# Область тер. управления
class lk_ty(lk_objects):
    def __init__(self):
        super().__init__()
        self.actionlist = {
            'allproblem': self.b1,
        }

    def b1(self): #Все обращения
        userlk = self.request.user
        self.prob = Problem.objects.filter((Q(visible='1') & Q(statussys='1')) & Q(ciogv=userlk.userprofile.ty))


ns = {
    'ty': lk_ty,
    'moderator': lk_moderator,
    'dispatcher': lk_dispatcher,
    'executor': lk_executor
}


def prob_func(func):
    try:
        fun = ns[func.lower()]
    except:
        logger_error.error(traceback.format_exc())
    return fun
