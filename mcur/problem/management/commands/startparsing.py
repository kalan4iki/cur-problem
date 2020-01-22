# -*- coding: utf-8 -*-
#Исполняемый файл работы парсера
from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from xml.dom.minidom import parseString
from bs4 import BeautifulSoup
from sys import platform
#from bot.models import KNDhistor, DIPhistor, MKDhistor, Usersbot
#from gis.settings import DEBUG, username_knd, password_knd, path_driver, logi
from problem.models import Problem
import lxml
import time
import datetime
import logging
import argparse
import traceback
'''
def parser():
    now = datetime.datetime.now()
    times = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
    if now.day < 10:
        tinow = "0" + str(now.day) + "." + str(now.month) + "." + str(now.year)
    else:
        tinow = str(now.day) + "." + str(now.month) + "." + str(now.year)
    opts = Options()
    if platform == 'linux' or platform == 'linux2':
        opts.add_argument('headless')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(path_driver['linux'],options=opts)
    elif platform == 'win32':
        driver = webdriver.Chrome(path_driver['win'], options=opts)
    driver.get("https://knd.mosreg.ru/snowfalls")
    time.sleep(5)
    driver.find_element_by_id('userName').clear()
    driver.find_element_by_id('userName').send_keys(username_knd)
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys(password_knd)
    driver.find_element_by_xpath('/html/body/div/form/div[3]/div/div/span/button').click()
    time.sleep(10)
    a = driver.page_source
    soup = BeautifulSoup(a, 'lxml')
    div = soup.find_all('div', class_ = 'ant-col ant-col-14')
    driver.quit()
    temp = []
    proc = []
    sum = 0
    for i in div:
        a = i.text.split('%')
        b = int(a[1].split(' ')[-1].split(')')[0])
        temp.append(b)
        proc.append(float(a[0]))
        sum += b
    tisplit = tinow.split('.')
    a = KNDhistor(date = tinow, day=tisplit[0], month=tisplit[1], year=tisplit[2], allz= sum,
                    vrabote= temp[0], dost= temp[1], complete= temp[2], netreb= temp[3],
                    vraboteproc= proc[0], dostproc= proc[1], completeproc= proc[2], netrebproc= proc[3])
    a.save()
'''

def StartBrowser():
    opts = Options()
    driver = webdriver.Chrome('C:\chromedriver.exe', options=opts)
    return driver
    '''
    if platform == 'linux' or platform == 'linux2':
        opts.add_argument('headless')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(path_driver['linux'],options=opts)
    elif platform == 'win32':
        driver = webdriver.Chrome(path_driver['win'], options=opts)
    '''

def loginDobrodel(brow, url, date, vxod):
    browser = brow
    try:
        browser.get(url)
        time.sleep(2)
        browser.find_element_by_name('j_username').send_keys(vxod['username'])
        browser.find_element_by_name('j_password').send_keys(vxod['password'])
        browser.find_element_by_xpath('/html/body/div/div[2]/div/form/div/div[5]').click()
        time.sleep(5)
        browser.find_element_by_id('datefrom').clear()
        browser.find_element_by_id('datefrom').send_keys(date)
        browser.find_element_by_id('deadlineFrom').clear()
        browser.find_element_by_id('deadlineFrom').send_keys(date)
        browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[1]/form/div[10]/button').click()
        time.sleep(7)
        a = Select(browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[4]/div[1]/span[3]/select'))
        a.select_by_value('25')
        time.sleep(5)
    except:
        print(traceback.format_exc())
    return browser

if __name__ == '__main__':
    parser()

class Command(BaseCommand):
    help = 'Команда запуска парсера vmeste.mosreg.ru'

    def handle(self, *args, **options):
        #Инициализация браузера
        browser = StartBrowser()
        now = datetime.datetime.now()
        a = True
        loginDobrodel(browser, 'http://vmeste.mosreg.ru', '01.10.2019', {'username': 'smsv@istra-adm.ru', 'password': 'qwerty5512222'})
        try:
            source = browser.page_source
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
                prob = Problem(nomdobr=temp2[0],temat=temp2[5] + '. ' + temp2[6],text=temp2[3],adres=temp2[2],datecre=f'{date[2]}-{date[1]}-{date[0]}',status=temp2[13])
                prob.save()
                print(temp2)
            #print(table[0])
            print(len(table))
        except:
            print(traceback.format_exc())
        time.sleep(5)
        browser.quit()
