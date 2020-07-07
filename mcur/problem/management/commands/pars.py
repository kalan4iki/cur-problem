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

class parser:
    def __init__(self, *args, **kwargs):
        self.browser = kwargs['browser']
        self.status = 'Не онлайн'
        self.qs = dict()

    def start(self):
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

    def __str__(self):
        return f'Парсер со статусом {self.status}, зарегистророван под id {self.qs.pk}'
