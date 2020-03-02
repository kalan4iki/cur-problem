# -*- coding: utf-8 -*-
#Исполняемый файл работы парсера
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from sys import platform
from problem.models import Problem, Category, Podcategory, Status
from parsers.models import Parser, ActionHistory
from parsers.models import Status as StatusPars
import time
import datetime
import traceback


def StartBrowser():
    opts = Options()
    if platform == 'linux' or platform == 'linux2':
        opts.add_argument('headless')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('/home/chromedriver', options=opts)
    else:
        driver = webdriver.Chrome('C:\chromedriver.exe', options=opts)
    a = Parser(session=driver.session_id, name='Парсер', status=StatusPars.objects.get(name='Online'))
    a.save()
    return driver


def loginDobrodel(brow, url, vxod):
    browser = brow
    try:
        browser.get(url)
        time.sleep(2)
        browser.find_element_by_name('j_username').send_keys(vxod['username'])
        browser.find_element_by_name('j_password').send_keys(vxod['password'])
        browser.find_element_by_xpath('/html/body/div/div[2]/div/form/div/div[5]').click()
        time.sleep(5)
    except:
        print(traceback.format_exc())

def parsingall(browser, date):
        browser.find_element_by_id('datefrom').clear()
        browser.find_element_by_id('datefrom').send_keys(date)
        browser.find_element_by_id('deadlineFrom').clear()
        browser.find_element_by_id('deadlineFrom').send_keys(date)
        browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[1]/form/div[10]/button').click()
        time.sleep(7)
        a = Select(browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[4]/div[1]/span[3]/select'))
        a.select_by_value('25')
        time.sleep(5)
        bs = BeautifulSoup(browser.page_source, 'lxml')
        sele = bs.find('span', class_='jtable-goto-page').find('select').find_all('option')
        pages = []
        for i in sele:
            pages.append(i.text)
        return pages



def parsTable(source):
    try:
        bs = BeautifulSoup(source, 'lxml')
        table = bs.find_all('tr', class_ = 'jtable-data-row')
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
            if not Podcategory.objects.filter(name=temp2[6]).exists():
                podcat = Podcategory(name=temp2[6], categ=Category.objects.get(name=temp2[5]))
                podcat.save()
            if not Status.objects.filter(name=temp2[13]).exists():
                stat = Status(name=temp2[13])
                stat.save()
            else:
                stat = Status.objects.get(name=temp2[13])
            visi = '1'
            if temp2[13] == 'Закрыто' and temp2[13] == 'Решено' and temp2[13] == 'Получен ответ':
                visi = '0'
            if not Problem.objects.filter(nomdobr=temp2[0]).exists():
                prob = Problem(nomdobr=temp2[0], temat=Category.objects.get(name=temp2[5]),
                               podcat=Podcategory.objects.get(name=temp2[6]), text=temp2[3], adres=temp2[2],
                               datecre=f'{date[2]}-{date[1]}-{date[0]}', status=stat, parsing='1',
                               dateotv=f'{date2[2]}-{date2[1]}-{date2[0]}', visible=visi)
            else:
                prob = Problem.objects.get(nomdobr=temp2[0])
                prob.temat = Category.objects.get(name=temp2[5])
                prob.podcat = Podcategory.objects.get(name=temp2[6])
                prob.text = temp2[3]
                prob.adres = temp2[2]
                prob.datecre = f'{date[2]}-{date[1]}-{date[0]}'
                prob.dateotv = f'{date2[2]}-{date2[1]}-{date2[0]}'
                prob.status = stat
                prob.parsing = '1'
                prob.visible = visi
            prob.save()
            return prob
    except:
        print(traceback.format_exc())


def pars(browser, nom):
    browser.find_element_by_id('datefrom').clear()
    browser.find_element_by_id('deadlineFrom').clear()
    browser.find_element_by_id('id').clear()
    browser.find_element_by_id('id').send_keys(nom)
    browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[1]/form/div[10]/button').click()
    time.sleep(1)


class Command(BaseCommand):
    help = 'Команда запуска парсера vmeste.mosreg.ru'

    #add_arguments(self, parser):
        #parser.add_argument('-mode', dest='mode', nargs='+', type=int)

    def handle(self, *args, **options):
        browser = StartBrowser() #Инициализация браузера
        loginDobrodel(browser, 'http://vmeste.mosreg.ru', {'username': 'tsa@istra-adm.ru', 'password': '12345678'})
        a = True
        while a:
            b = ActionHistory.objects.filter(status='0')
            if len(b) > 0:
                for i in b:
                    if i.act.nact == '1':
                        print('0')
                        if i.arg != None:
                            kolvo = parsingall(browser, '01.01.2019')
                            for i in kolvo:
                                sele = Select(browser.find_element_by_xpath('//*[@id="Container"]/div/div[4]/div[1]/span[2]/select'))
                                sele.select_by_value(i)
                                time.sleep(5)
                                source = browser.page_source
                                parsTable(source)
                    elif i.act.nact == '2':
                        print('1')
                        if i.arg == None:
                            prob = Problem.objects.filter(visible='1')
                            for i in prob:
                                pars(browser, i.nomdobr)
                                source = browser.page_source
                                temp = parsTable(source)
                                try:
                                    if i.status.name != temp.status.name:
                                        print(f'Жалоба №{i.nomdobr}: Был статус: {i.status}, теперь {temp.status}')
                                except:
                                    print(traceback.format_exc())
                        else:
                            print('2')
                            pars(browser, i.arg)
                            source = browser.page_source
                            parsTable(source)
                    i.status = '1'
                    i.save()
        time.sleep(2)
        browser.quit()