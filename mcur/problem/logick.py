from .models import (Problem, Term, Answer, Status, Termhistory)
from django.db.models import Q
from datetime import date, timedelta, datetime

# Область исполнителя
class lk_executor:
    def b1(request, act): # Ответы
        userlk = request.user
        q1 = Q(user=userlk)
        termas = Answer.objects.filter(q1)
        termas2 = Term.objects.filter(answers__in=termas)
        prob = Problem.objects.filter(visible='1', terms__in=termas2)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b2(request, act): # Все обращения
        userlk = request.user
        if userlk.userprofile.dep == None:
            q1 = Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk)
        else:
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
            termas = Termhistory.objects.filter(q1)
            q1 = Q(curat=userlk.userprofile.dep) | Q(curatuser=userlk)
        termas2 = Term.objects.filter((q1 | Q(resolutions__in=termas)) & (Q(status='0') | Q(status='1')))
        prob = Problem.objects.filter((Q(visible='1') & Q(statussys='1')) & Q(terms__in=termas2))
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b3(request, act): # Подходит срок
        userlk = request.user
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
        prob = Problem.objects.filter(Q(terms__in=termas1) & q21 & q2)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b4(request, act): # Обращения на сегодня
        userlk = request.user
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
        #q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        q21 = Q(dateotv=nowdate)
        prob = Problem.objects.filter((Q(terms__in=termas1) & q21) & q2)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b5(request, act): # Просроченные
        userlk = request.user
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
        prob = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b6(request, act): # Мои обращения
        userlk = request.user
        q1 = Q(curatuser=userlk)
        termas = Term.objects.filter(q1)
        prob = Problem.objects.filter(Q(terms__in=termas) & Q(visible='1'))
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

# Область диспетчера
class lk_dispatcher:
    def b1(request, act): #Все обращения
        userlk = request.user
        org = userlk.userprofile.org
        q1 = Q(curatuser=userlk)
        termas = Termhistory.objects.filter(q1)
        q1 = (Q(org=org) | Q(curat__org=org) | Q(curatuser=userlk))
        termas2 = Term.objects.filter((q1 | Q(resolutions__in=termas)) & (Q(status='0') | Q(status='1')))
        termas3 = Problem.objects.filter(Q(visible='1') & Q(terms__in=termas2))
        if act == 1:
            kolvo = len(termas3)
            return kolvo
        elif act == 2:
            return termas3

    def b2(request, act): #Ответы
        userlk = request.user
        q1 = Q(user=userlk)
        termas = Answer.objects.filter(q1)
        termas2 = Term.objects.filter(answers__in=termas)
        termas3 = Problem.objects.filter(visible='1', terms__in=termas2)
        if act == 1:
            kolvo = len(termas3)
            return kolvo
        elif act == 2:
            return termas3

    def b3(request, act): #Подходит срок
        userlk = request.user
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
        termas2 = Problem.objects.filter((q1 | (q2 & q3) | q4) & q5)
        if act == 1:
            kolvo = len(termas2)
            return kolvo
        elif act == 2:
            return termas2

    def b4(request, act): #Обращения на сегодня
        userlk = request.user
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
        termas2 = Problem.objects.filter((q1 | (q2 & q3) | q4) & q5)
        if act == 1:
            kolvo = len(termas2)
            return kolvo
        elif act == 2:
            return termas2

    def b5(request, act): #Просроченные
        userlk = request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        q1 = Q(curatuser=userlk)
        termas = Termhistory.objects.filter(q1)
        q1 = Q(org=userlk.userprofile.org) | Q(curatuser=userlk) | Q(curat__org=userlk.userprofile.org)
        q2 = (Q(status='0') | Q(status='1')) & Q(date__range=(date(2019, 1, 1), nowdate - timedelta(1)))
        termas1 = Term.objects.filter(q1 & q2 | Q(resolutions__in=termas))
        q2 = Q(visible='1') & Q(statussys='1')
        q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
        termas2 = Problem.objects.filter((Q(terms__in=termas1) | q21) & q2)
        if act == 1:
            kolvo = len(termas2)
            return kolvo
        elif act == 2:
            return termas2

# Область модератора
class lk_moderator:
    def b1(request, act): #Ответы
        userlk = request.user
        prob = Problem.objects.filter(visible='1', statussys='2', terms__answers__user=userlk)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b2(request, act): #Не распределенные
        userlk = request.user
        #prob = Problem.objects.filter(visible='1', statussys='2')
        prob = Problem.objects.filter(Q(visible='1') & Q(terms=None))
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b3(request, act): # Все обращения
        userlk = request.user
        prob = Problem.objects.filter(visible='1')
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b4(request, act): # Мои обращения
        userlk = request.user
        q1 = Q(curatuser=userlk)
        termas = Term.objects.filter(q1)
        prob = Problem.objects.filter(Q(terms__in=termas) & Q(visible='1'))
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b5(request, act): # Подходит срок
        userlk = request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        q1 = (Q(status='0') | Q(status='1')) & Q(date__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        q21 = Q(dateotv__range=(nowdate + timedelta(1), nowdate + timedelta(4)))
        q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
            status__in=Status.objects.filter(name='Указан срок')))
        termas = Term.objects.filter(q1)
        prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b6(request, act): # Обращения на сегодня
        userlk = request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        q1 = (Q(status='0') | Q(status='1')) & Q(date=nowdate)
        q21 = Q(dateotv=nowdate)
        q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
            status__in=Status.objects.filter(name='Указан срок')))
        termas = Term.objects.filter(q1)
        prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b7(request, act): # Просроченные
        userlk = request.user
        nowdatetime = datetime.now()
        nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
        q1 = (Q(status='0') | Q(status='1')) & Q(
            date__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
        q21 = Q(dateotv__range=(date(nowdatetime.year, 1, 1), nowdate - timedelta(1)))
        q22 = Q(visible='1') & (Q(status__in=Status.objects.filter(name='В работе')) | Q(
            status__in=Status.objects.filter(name='Указан срок')))
        termas = Term.objects.filter(q1)
        prob = Problem.objects.filter((Q(terms__in=termas) | q21) & q22)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b8(request, act): # ТУ лист
        userlk = request.user
        prob = Problem.objects.filter(Q(ciogv=None) & Q(visible='1'))
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob

    def b9(request, act):
        userlk = request.user
        term = Term.objects.filter(further=True).order_by('furtherdate')
        prob = Problem.objects.filter(terms__in=term)
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob


# Область тер. управления
class lk_ty:
    def b1(request, act): #Все обращения
        userlk = request.user
        prob = Problem.objects.filter((Q(visible='1') & Q(statussys='1')) & Q(ciogv=userlk.userprofile.ty))
        if act == 1:
            kolvo = len(prob)
            return kolvo
        elif act == 2:
            return prob