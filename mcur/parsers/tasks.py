from time import sleep
from .celery import app
from .models import ActionHistory, Action
from datetime import date, timedelta, datetime
import os
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

@app.task
def Everyday_restart(a):
    nowdatetime = datetime.now()
    nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
    action = [Action.objects.get(nact=8), Action.objects.get(nact=5), Action.objects.get(nact=2),
              Action.objects.get(nact=10)]
    a1 = ActionHistory()
    a1.act = action[0]
    a1.save()
    data = (nowdate - timedelta(3)).strftime('%d.%m.%Y')
    tempdate = nowdate.strftime('%d.%m.%Y')
    a2 = ActionHistory()
    a2.act = action[1]
    a2.arg = f'{data},{tempdate}'
    a2.save()
    a3 = ActionHistory()
    a3.act = action[2]
    a3.arg = 'all'
    a3.save()
    a4 = ActionHistory()
    a4.act = action[3]
    a4.save()



@app.task
def Everyday():
    nowdatetime = datetime.now()
    nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
    action = [Action.objects.get(nact=8), Action.objects.get(nact=5), Action.objects.get(nact=2),
              Action.objects.get(nact=10)]
    data = (nowdate - timedelta(3)).strftime('%d.%m.%Y')
    tempdate = nowdate.strftime('%d.%m.%Y')
    a2 = ActionHistory()
    a2.act = action[1]
    a2.arg = f'{data},{tempdate}'
    a2.save()
    a3 = ActionHistory()
    a3.act = action[2]
    a3.arg = 'all'
    a3.save()
    a4 = ActionHistory()
    a4.act = action[3]
    a4.save()