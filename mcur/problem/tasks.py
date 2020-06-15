from celery import Celery
from time import sleep
from sys import platform
app = Celery('tasks', backend='rpc://', broker='amqp://guest@localhost//')

@app.task
def Everyday_restart(a):
  if platform == 'linux' or platform == 'linux2':
    sleep(10) # поставим тут задержку в 10 сек для демонстрации ассинхрности
    print('Hello World' + str(a))


@app.task
def Everyday_restart(a):
  sleep(10) # поставим тут задержку в 10 сек для демонстрации ассинхрности
  print('Hello World' + str(a))