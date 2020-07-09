# -*- coding: utf-8 -*-
# Исполняемый файл работы парсера
if __name__ != '__main__':
    from django.core.management.base import BaseCommand
    from django.db.models import Q
    from problem.models import Problem, Category, Podcategory, Status, Image, Author
    from parsers.models import Parser, ActionHistory, Loggings
    from parsers.models import Status as StatusPars
    from mcur.settings import MEDIA_ROOT, MEDIA_URL, NO_VISIBLE, FULL_PARS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from sys import platform
from datetime import date, datetime
import xml.etree.ElementTree as xml
import time
import traceback
import logging


if __name__ != '__main__':
    logger = logging.getLogger('django.server')
    loggerfile = logging.getLogger('file')
    logger_mail = logging.getLogger('django.request')


class parser_save:
    def __init__(self, target, data, *args, **kwargs):
        self.target = target
        self.targets = {
            'problem': self.problem
        }
        self.data = data

    def problem(self):
        if Problem.objects.filter(nomdobr=self.data['nomdobr']).exists():
            prob = Problem.objects.get(nomdobr=self.data['nomdobr'])
            prob.temat = self.data['temat']
            prob.podcat = self.data['podcat']
            prob.text = self.data['text']
            prob.adres = self.data['adres']
            prob.datecre = self.data['datecre']
            prob.dateotv = self.data['dateotv']
            prob.status = self.data['status']
            prob.parsing = self.data['parsing']
            prob.visible = self.data['visible']
        else:
            prob = Problem(nomdobr=self.data['nomdobr'], temat=self.data['temat'], podcat=self.data['podcat'], text=self.data['text'],
                           adres=self.data['adres'], datecre=self.data['datecre'], status=self.data['status'], parsing=self.data['parsing'],
                           dateotv=self.data['dateotv'], visible=self.data['visible'], author=self.data['author'])



class parser:
    def __init__(self, *args, **kwargs):
        '''
            Функция инициализации парсера
        '''
        if 'login' in kwargs:
            self.login = kwargs['login']
        elif __name__ != '__main__':
            self.login = FULL_PARS['auth'][0]
        else:
            self.login = None
        if 'password' in kwargs:
            self.password = kwargs['password']
        elif __name__ != '__main__':
            self.password = FULL_PARS['auth'][1]
        else:
            self.password = None
        self.browser = None
        self.status = 'Не онлайн'
        self.qs = dict()
        if __name__ != '__main__':
            self.starturl = FULL_PARS['start_url']
            self.namepol = FULL_PARS['form_fileds']
        else:
            self.starturl = 'https://vmeste.mosreg.ru/login'
            self.namepol = {'nomdobr': ['id'],'date': ['datefrom', 'dateto'],'cdate': ['cdatefrom', 'cdateto'],'deadline': ['deadlineFrom', 'deadlineTo']}
        self.source = ''
        self.note = ''
        self.kolerror = 0
        self.actionlist = {
            'start': [self.start, 0],
            'loginsait': [self.loginsait, 0],
            'clearall': [self.clearall, 0]
        }

    def launch(self):
        '''
            Функция запуска парсера и авторизации на сайте
        '''
        self.status = 'Инициализация запуска парсера'
        b = 0
        nam = ''
        try:
            for i in self.actionlist:
                nam = i
                self.actionlist[i][1] = self.actionlist[i][0]()
        except:
            self.errors(tb=traceback.format_exc())
            self.actionlist[nam][1] = 1
            if self.browser != None:
                self.quit()
            return 1
        self.status = 'Парсер запущен'

    def start(self):
        self.status = 'Запуск парсера'
        opts = Options()
        if platform == 'linux' or platform == 'linux2':
            opts.add_argument('headless')
            opts.add_argument('--no-sandbox')
            opts.add_argument('--disable-dev-shm-usage')
            self.browser = webdriver.Chrome('/home/chromedriver', options=opts)
        else:
            self.browser = webdriver.Chrome('C:\chromedriver.exe', options=opts)
        if __name__ != '__main__':
            a = Parser(session=self.browser.session_id, name='Парсер', status=StatusPars.objects.get(name='Online'))
            a.save()
            self.qs = a
            self.note = f'Парсер номер: {self.qs.pk}'
        self.status = 'Парсер запущен'
        return 0

    def loginsait(self):
        self.status = 'Авторизация на сайте'
        self.browser.get(self.starturl)
        time.sleep(2)
        self.browser.find_element_by_name('j_username').send_keys(self.login)
        self.browser.find_element_by_name('j_password').send_keys(self.password)
        self.browser.find_element_by_xpath('/html/body/div/div[2]/div/form/div/div[5]').click()
        self.status = 'Парсер авторизован'
        time.sleep(5)
        return 0

    def clearall(self):
        for i in self.namepol:
            for j in self.namepol[i]:
                self.browser.find_element_by_id(j).clear()

    def pars_table(self):
        self.get_source()
        bs = BeautifulSoup(self.source, 'lxml')
        bs.find()
        table = bs.find_all('tr', class_='jtable-data-row')
        if len(table) > 0:
            for i in table:
                temp = i.find_all('td')
                temp2 = []
                iter = 0
                for j in temp:
                    if iter == 3:
                        temp2.append(j.find('a').attrs['data-hint'])
                    else:
                        temp2.append(j.text)
                    iter += 1
                date = temp2[9].split('.')
                date2 = temp2[11].split('.')
                if not Category.objects.filter(name=temp2[5]).exists():
                    cat = Category(name=temp2[5])
                    cat.save()
                else:
                    cat = Category.objects.get(name=temp2[5])
                if not Podcategory.objects.filter(name=temp2[6]).exists():
                    podcat = Podcategory(name=temp2[6], categ=Category.objects.get(name=temp2[5]))
                    podcat.save()
                else:
                    podcat = Podcategory.objects.get(name=temp2[6])
                if not Status.objects.filter(name=temp2[13]).exists():
                    stat = Status(name=temp2[13])
                    stat.save()
                else:
                    stat = Status.objects.get(name=temp2[13])
                visi = '1'
                if stat.pk in NO_VISIBLE[0]:
                    visi = '0'
                elif stat.pk in NO_VISIBLE[1]:
                    visi = '2'
                data = {}
                data['nomdobr'] = temp2[0]
                data['temat'] = cat
                data['podcat'] = podcat
                data['text'] = temp2[3]
                data['adres'] = temp2[2]
                data['datecre'] = f'{date[2]}-{date[1]}-{date[0]}'
                data['dateotv'] = f'{date2[2]}-{date2[1]}-{date2[0]}'
                data['status'] = stat
                data['parsing'] = '1'
                data['visible'] = visi

    def pars_card(self):
        pass

    def quit(self):
        self.browser.close()
        self.browser.quit()
        self.status = 'Парсер выключен'

    def errors(self, *args, **kwargs):
        if 'tb' in kwargs:
            print(kwargs['tb'])
        self.kolerror += 1
        if self.kolerror <= 3:
            self.status = 'Ошибка парсера, перезагрузка.'
            self.launch()
        else:
            self.quit()
            self.status = 'Постоянная ошибка. Парсер отключен.'

    def get_source(self):
        self.source = self.browser.page_source

    def __str__(self):
        return f'Парсер со статусом {self.status}, зарегистророван под id {self.qs.pk}'

    def __call__(self):
        pass


if __name__ == '__main__':
    login = input('Введите логин добродела: ')
    pasw = input('Введите пароль добродела: ')
    a = parser(login=login, password=pasw)
    a.launch()
    time.sleep(10)
    a.quit()
