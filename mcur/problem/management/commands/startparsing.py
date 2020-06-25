# -*- coding: utf-8 -*-
#Исполняемый файл работы парсера
from django.core.management.base import BaseCommand
from django.db.models import Q
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from sys import platform
from problem.models import Problem, Category, Podcategory, Status, Image, Author
from parsers.models import Parser, ActionHistory, Loggings
from parsers.models import Status as StatusPars
from mcur.settings import MEDIA_ROOT, MEDIA_URL, NO_VISIBLE
from datetime import date, datetime
import xml.etree.ElementTree as xml
import time
import traceback
import logging


logger = logging.getLogger('django.server')
loggerfile = logging.getLogger('file')
logger_mail = logging.getLogger('django.request')

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


class RefreshProblem(object):

    def __init__(self, *args, **kwargs):
        temp = ''


def parsProblem(browser, prob=None):
        url = 'https://vmeste.mosreg.ru/CardInNewPage?show=/Topic?id='
        if prob == None:
            prob = Problem.objects.filter((Q(visible='1') | Q(visible='2')) & Q(author=None))
            print(f'Начало парсинга авторов, количество обращение: {len(prob)}')
        for i in prob:
            if i.author == None:
                nom = i.nomdobr
                browser.get(f'{url}{nom}')
                time.sleep(2)
                source = browser.page_source
                bs = BeautifulSoup(source, 'lxml')
                prov = bs.find('div', class_='left')
                if len(prov) > 0:
                    proverka = prov.text
                    if len(proverka.split('№')) == 2:
                        if nom == proverka.split('№')[1]:
                            fio = bs.find('div', class_='t-user-name').text
                            a = None
                            tel = None
                            email = None
                            dop = bs.find_all('div', class_='t-user-email')
                            dops = []
                            for j in dop:
                                temp = j.text
                                if temp != '':
                                    dops.append(temp)
                            if len(dops) == 0:
                                if Author.objects.filter(fio=fio).exists():
                                    a = Author.objects.get(fio=fio)
                                else:
                                    a = Author(fio=fio)
                                    a.save()
                                    loggerfile.info(f'[PARSER][INFO]: Создан автор {a.pk} - {fio}')
                            elif len(dops) > 1:
                                email = dops[0]
                                tel = dops[1].split(':')[1].replace(' ', '')
                                if Author.objects.filter(email=email).exists():
                                    a = Author.objects.get(email=email)
                                else:
                                    a = Author(fio=fio, email=email, tel=tel)
                                    a.save()
                                    loggerfile.info(f'[PARSER][INFO]: Создан автор {a.pk} - {fio} - {email} - {tel}')
                            else:
                                if dops[0].find('@') != -1:
                                    email = dops[0]
                                    if Author.objects.filter(email=email).exists():
                                        a = Author.objects.get(email=email)
                                    else:
                                        a = Author(fio=fio, email=email)
                                        a.save()
                                        loggerfile.info(f'[PARSER][INFO]: Создан автор {a.pk} - {fio} - {email}')
                                else:
                                    tel = dops[0].split(':')[1].replace(' ', '')
                                    if Author.objects.filter(tel=tel).exists():
                                        a = Author.objects.get(tel=tel)
                                    else:
                                        a = Author(fio=fio, tel=tel)
                                        a.save()
                                        loggerfile.info(f'[PARSER][INFO]: Создан автор {a.pk} - {fio} - {tel}')
                            i.author = a
                            i.save()
                            loggerfile.info(f'[PARSER][INFO]: Создана связь [обращение {i.nomdobr} - автор {a.pk}]')
                        else:
                            logger.error(f'[PARSER][ERROR]: Не совпадение обращения {nom}.')
                    else:
                        logger.error(f'[PARSER][ERROR]: Не найдено id.')
                else:
                    logger.error(f'[PARSER][ERROR]: обращение {nom} на сайте не найдено.')
        urls = 'http://vmeste.mosreg.ru'
        browser.get(urls)
        time.sleep(2)


def parsingall(browser, date, dopos):
    browser.find_element_by_id('datefrom').clear()
    browser.find_element_by_id('dateto').clear()
    browser.find_element_by_id('deadlineFrom').clear()
    browser.find_element_by_id('deadlineTo').clear()
    browser.find_element_by_id('id').clear()
    if dopos == '0':
        browser.find_element_by_id('datefrom').send_keys(date)
        browser.find_element_by_id('deadlineFrom').send_keys(date)
    elif dopos == '1':
        browser.find_element_by_id('dateto').send_keys(date)
    elif dopos == '2':
        browser.find_element_by_id('datefrom').send_keys(date[0])
        browser.find_element_by_id('dateto').send_keys(date[1])
    elif dopos == '3':
        browser.find_element_by_id('deadlineFrom').send_keys(date)
    elif dopos == '4':
        browser.find_element_by_id('deadlineFrom').send_keys(date[0])
        browser.find_element_by_id('deadlineTo').send_keys(date[1])
    browser.find_element_by_id('id').click()
    browser.find_element_by_id('LoadRecordsButton').click()
    time.sleep(7)
    a = Select(browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[4]/div[1]/span[3]/select'))
    a.select_by_value('25')
    time.sleep(5)


class CardParse(object):
    actionqs = []
    xmlcard = xml.Element("main")
    act = xml.Element('Action')
    problems = xml.Element('Problem')

    def __init__(self, *args, **kwargs):
        self.actionqs = kwargs['action']
        self.xmlcard.append(self.act)
        self.xmlcard.append(self.problems)
        actid = xml.SubElement(self.act, "id")
        actid.text = str(self.actionqs.pk)
        actname = xml.SubElement(self.act, "name")
        actname.text = str(self.actionqs.act)
        actarg = xml.SubElement(self.act, "arg")
        actarg.text = str(self.actionqs.arg)


    def update(self, data):
        id = xml.Element(data['nomdobr'])
        self.xmlcard.append(id)
        newstatus = xml.SubElement(id, 'newstatus')
        newstatus.text = data['status'].name
        laststatus = xml.SubElement(id, 'laststatus')
        success = xml.SubElement(id, 'success')
        temp = ''
        if Problem.objects.filter(nomdobr=data['nomdobr']).exists():
            prob = Problem.objects.get(nomdobr=data['nomdobr'])
            laststatus.text = prob.status.name
            prob.temat = data['temat']
            prob.podcat = data['podcat']
            prob.text = data['text']
            prob.adres = data['adres']
            prob.datecre = data['datecre']
            prob.dateotv = data['dateotv']
            prob.status = data['status']
            prob.parsing = data['parsing']
            prob.visible = data['visible']
        else:
            prob = Problem(nomdobr=data['nomdobr'], temat=data['temat'], podcat=data['podcat'], text=data['text'],
                           adres=data['adres'], datecre=data['datecre'], status=data['status'], parsing=data['parsing'],
                           dateotv=data['dateotv'], visible=data['visible'])
        prob.save()
        prob = Problem.objects.get(nomdobr=data['nomdobr'])
        if prob.status == data['status']:
            success.text = 'Successfully'
        else:
            success.text = 'Unsuccessfully'


    def close(self, **kwargs):
        if 'error' in kwargs:
            errors = xml.Element('Errors')
            self.xmlcard.append(errors)
        path = MEDIA_ROOT + 'cardpars/'
        fn = f'act-{self.actionqs.pk}.xml'
        tree = xml.ElementTree(self.xmlcard)
        with open(path + fn, 'wb') as fh:
            tree.write(fh, encoding="utf-8")


def parsTable(source, card):
    try:
        bs = BeautifulSoup(source, 'lxml')
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
                card.update(data=data)
        else:
            return 'non'
    except:
        print(traceback.format_exc())


def pars(browser, nom):
    browser.find_element_by_id('datefrom').clear()
    browser.find_element_by_id('deadlineFrom').clear()
    browser.find_element_by_id('deadlineTo').clear()
    browser.find_element_by_id('dateto').clear()
    browser.find_element_by_id('id').clear()
    browser.find_element_by_id('id').click()
    browser.find_element_by_id('id').send_keys(nom)
    browser.find_element_by_id('LoadRecordsButton').click()
    time.sleep(1)


def debugs():
    opts = Options()
    browser = webdriver.Chrome('C:\chromedriver.exe', options=opts)
    url = 'http://vmeste.mosreg.ru'
    username = 'tsa@istra-adm.ru'
    password = '12345678'
    loginDobrodel(browser, url, {'username': username, 'password': password})
    return browser


class Command(BaseCommand):
    help = 'Команда запуска парсера vmeste.mosreg.ru'

    def handle(self, *args, **options):
        browser = StartBrowser() #Инициализация браузера
        url = 'http://vmeste.mosreg.ru'
        username = 'tsa@istra-adm.ru'
        password = '12345678'
        loginDobrodel(browser, url, {'username': username, 'password': password})
        a = True
        while a:
            b = ActionHistory.objects.filter(status='0')
            if len(b) > 0:
                for i in b:
                    card = CardParse(action=i)
                    try:
                        if i.act.nact == '1':#Просмотреть все жалобы
                            if i.arg != None:
                                parsingall(browser, i.arg, '0')
                                j = 1
                                while True:
                                    i.note = f'Страница {j}'
                                    i.save()
                                    source = browser.page_source
                                    parsTable(source, card)
                                    ele = browser.find_element_by_class_name('jtable-page-number-next')
                                    if ele.get_attribute('class') == 'jtable-page-number-next jtable-page-number-disabled':
                                        break
                                    else:
                                        ele.click()
                                    j += 1
                                    time.sleep(2)
                        elif i.act.nact == '2':#Посмотреть не закрытые жалобы
                            if i.arg == 'all':
                                prob = Problem.objects.filter(Q(visible='1') | Q(visible='2')).order_by('-dateotv')
                                als = len(prob)
                                ke = 1
                                for j in prob:
                                    i.note = f'Проблем {ke} их {als}'
                                    pars(browser, j.nomdobr)
                                    source = browser.page_source
                                    temp = parsTable(source, card)
                                    i.save()
                                    ke += 1
                                    if temp == 'non':
                                        j.visible = '0'
                                        j.note = 'Жалоба не найдена на сайте vmeste.mosreg.ru'
                                        j.save()
                            else:
                                pars(browser, i.arg)
                                source = browser.page_source
                                er = parsTable(source, card)
                                if er == 'non':
                                    tempsss = Problem.objects.get(nomdobr=i.arg)
                                    tempsss.visible = '0'
                                    tempsss.note = 'Жалоба не найдена на сайте vmeste.mosreg.ru. Индивидуальное обновление.'
                                    i.note = 'Жалоба скрыта.'
                                    i.save()
                                    tempsss.save()
                                else:
                                    i.note = 'Жалоба обновлена.'
                                    i.save()
                        elif i.act.nact == '3':#Выключить парсер
                            i.status = '1'
                            i.save()
                            break
                        elif i.act.nact == '4':#Посмотреть до определенного момента
                            if i.arg != None:
                                parsingall(browser, i.arg, '1')
                                j = 1
                                while True:
                                    ele = browser.find_element_by_class_name('jtable-page-number-next')
                                    i.note = f'Страница {j}'
                                    i.save()
                                    source = browser.page_source
                                    parsTable(source, card)
                                    if ele.get_attribute('class') == 'jtable-page-number-next jtable-page-number-disabled':
                                        break
                                    else:
                                        ele.click()
                                    j += 1
                                    time.sleep(2)
                        elif i.act.nact == '5':#Посмотреть временной промежуток
                            if i.arg != None:
                                tempdate = i.arg.split(',')
                                parsingall(browser, tempdate, '2')
                                j = 1
                                while True:
                                    ele = browser.find_element_by_class_name('jtable-page-number-next')
                                    i.note = f'Страница {j}'
                                    i.save()
                                    source = browser.page_source
                                    parsTable(source, card)
                                    if ele.get_attribute('class') == 'jtable-page-number-next jtable-page-number-disabled':
                                        break
                                    else:
                                        ele.click()
                                    j += 1
                                    time.sleep(2)
                        elif i.act.nact == '6':#Посмотреть срок решения от
                            if i.arg != None:
                                datetemp = i.arg.split(',')
                                if len(datetemp) == 1:
                                    parsingall(browser, i.arg, '3')
                                    j = 1
                                    while True:
                                        ele = browser.find_element_by_class_name('jtable-page-number-next')
                                        i.note = f'Страница {j}'
                                        i.save()
                                        source = browser.page_source
                                        parsTable(source, card)
                                        if ele.get_attribute('class') == 'jtable-page-number-next jtable-page-number-disabled':
                                            break
                                        else:
                                            ele.click()
                                        j += 1
                                        time.sleep(2)
                                elif len(datetemp) == 2:
                                    parsingall(browser, datetemp, '4')
                                    j = 1
                                    while True:
                                        ele = browser.find_element_by_class_name('jtable-page-number-next')
                                        i.note = f'Страница {j}'
                                        i.save()
                                        source = browser.page_source
                                        parsTable(source, card)
                                        if ele.get_attribute(
                                                'class') == 'jtable-page-number-next jtable-page-number-disabled':
                                            break
                                        else:
                                            ele.click()
                                        j += 1
                                        time.sleep(2)
                        elif i.act.nact == '7':#Обновить сегодняшние жалобы
                            nowdatetime = datetime.now()
                            nowdate = date(nowdatetime.year, nowdatetime.month, nowdatetime.day)
                            prob = Problem.objects.filter(visible='1', dateotv=nowdate)
                            als = len(prob)
                            ke = 1
                            for j in prob:
                                i.note = f'Проблем {ke} их {als}'
                                pars(browser, j.nomdobr)
                                source = browser.page_source
                                temp = parsTable(source, card)
                                i.save()
                                ke += 1
                                if temp == 'non':
                                    j.visible = '0'
                                    j.note = 'Жалоба не найдена на сайте vmeste.mosreg.ru'
                                    j.save()
                        elif i.act.nact == '8':#Обновление браузера
                            session = browser.session_id
                            parsers = Parser.objects.get(session=session)
                            parsers.delete()
                            browser.close()
                            browser.quit()
                            browser = StartBrowser()  # Инициализация браузера
                            url = 'http://vmeste.mosreg.ru'
                            username = 'tsa@istra-adm.ru'
                            password = '12345678'
                            loginDobrodel(browser, url, {'username': username, 'password': password})
                        elif i.act.nact == '9':#Получить скриншот
                            nowdatetime = datetime.now()
                            name = f'{nowdatetime.day}{nowdatetime.month}{nowdatetime.year}{nowdatetime.hour}{nowdatetime.minute}.png'
                            url = MEDIA_ROOT+'photos/' + name
                            a = browser.save_screenshot(url)
                            i.note = 'https://skiog.ru' + MEDIA_URL+'photos/' + name
                            i.save()
                        elif i.act.nact == '10':#Парсинг авторов
                            prob = Problem.objects.filter((Q(visible='1') | Q(visible='2')) & Q(author=None))
                            i.note = f'Обращений {len(prob)}'
                            i.save()
                            parsProblem(browser, prob)
                        elif i.act.nact == '11':  # Парсинг авторов
                            prob = Problem.objects.filter(visible='0', status__pk=6).order_by('-datecre')
                            als = len(prob)
                            ke = 1
                            for j in prob:
                                i.note = f'Проблем {ke} их {als}'
                                pars(browser, j.nomdobr)
                                source = browser.page_source
                                temp = parsTable(source, card)
                                i.save()
                                ke += 1
                                if temp == 'non':
                                    j.visible = '0'
                                    j.note = 'Жалоба не найдена на сайте vmeste.mosreg.ru'
                                    j.save()
                        i.status = '1'
                        i.save()
                        card.close()
                    except:
                        i.status = '2'
                        i.save()
                        card.close(error='error')
                        logger.info('[PARSER]: ' + traceback.format_exc())
                        logger_mail.error('[PARSER]: ' + traceback.format_exc())
        time.sleep(2)
        browser.close()
        browser.quit()