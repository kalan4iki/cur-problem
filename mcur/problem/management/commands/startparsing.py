# -*- coding: utf-8 -*-
#Исполняемый файл работы парсера
from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from xml.dom.minidom import parseString
from bs4 import BeautifulSoup
from sys import platform
from bot.models import KNDhistor, DIPhistor, MKDhistor, Usersbot
from gis.settings import DEBUG, username_knd, password_knd, path_driver, logi
import lxml
import time
import datetime
import logging
import argparse
import traceback

if platform == 'linux' or platform == 'linux2':
    logging.basicConfig(filename=logi['linux']['direct']+logi['linux']['parser'], level=logging.INFO)
elif platform == 'win32':
    logging.basicConfig(filename=logi['win']['direct']+logi['win']['parser'], level=logging.INFO)


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

if __name__ == '__main__':
    parser()

class Command(BaseCommand):
    help = 'Команда запуска парсера KND'

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        a = True
        while a:
            now = datetime.datetime.now()
            times = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
            if now.hour < 21 or now.hour > 6:
                try:
                    parser()
                except:
                    logging.error('Parser ' + times + " Error data: " + traceback.format_exc())
                time.sleep(900)
