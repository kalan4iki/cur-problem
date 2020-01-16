from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Curator(models.Model):
    name = models.CharField(max_length=40, help_text='Куратор проблемы',
                            verbose_name = 'Куратор')

    class Meta:
        ordering = ['name']
        verbose_name = 'куратор проблемы'
        verbose_name_plural = 'кураторы проблем'
        #permissions = {"", }

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("curators", args=(self.pk,))

class Access(models.Model):
    lvls = {
        ('r','Чтение'),
        ('w','Запись'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    dost = models.ManyToManyField(Curator, verbose_name = 'Организация')
    lvl = models.CharField(max_length=40, help_text='Уровень доступа', verbose_name = 'Уровень доступа',
                            choices=lvls)
                            
    class Meta:
        ordering = ['user']
        verbose_name = 'доступ'
        verbose_name_plural = 'доступы'
        #permissions = {"", }

    def __str__(self):
        return self.user

class Minis(models.Model):
    name = models.CharField(max_length=40, help_text='ЦИОГВ',
                            verbose_name = 'ЦИОГВ')

    class Meta:
        ordering = ['name']
        verbose_name = 'ЦИОГВ'
        verbose_name_plural = 'ЦИОГВ'

    def __str__(self):
        return self.name

class Term(models.Model):
    date = models.DateField(help_text='Срок', verbose_name = 'Срок', null=True)
    curat = models.ForeignKey(Curator, on_delete = models.PROTECT,
                            help_text='Куратор', verbose_name = 'Куратор')
    desck = models.TextField(help_text='Описание', verbose_name = 'Описание', blank=True, null=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'срок жалобы'
        verbose_name_plural = 'сроки жалоб'

    def __str__(self):
        temp = f'{self.curat} - {self.date.day}.{self.date.month}.{self.date.year}'
        return temp

    def get_absolute_url(self):
        return reverse("curators", args=(self.curat.pk,))

class Problem(models.Model):
    nomdobr = models.CharField(max_length = 20, help_text = 'Номер проблемы',
                            verbose_name = 'Номер', unique = True)
    temat = models.CharField(max_length=20, help_text='Тематика проблемы',
                            verbose_name = 'Тематика', blank=True, null=True)
    ciogv = models.ForeignKey(Minis, on_delete = models.PROTECT, blank=True,
                            help_text='ЦИОГВ', verbose_name = 'ЦИОГВ', null=True)
    text = models.TextField(help_text='Текст проблемы', verbose_name = 'Текст', blank=True, null=True)
    adres = models.CharField(max_length=255, help_text='Адрес проблемы',
                            verbose_name = 'Адрес', blank=True, null=True)
    url = models.URLField(help_text='URL проблемы', verbose_name = 'URL', blank=True, null=True)
    datecre = models.DateField(help_text='Дата создания', verbose_name = 'Дата создания', blank=True, null=True)
    datecrok = models.ManyToManyField(Term, help_text='Срок задачи', verbose_name = 'Срок задачи', blank=True, null=True)
    dateotv = models.DateField(help_text='Дата ответа исполнителя', verbose_name = 'Дата ответа исполнителя', blank=True, null=True)
    status = models.CharField(max_length=50, help_text='Статус проблемы',
                            verbose_name = 'Статус', blank=True, null=True)
    parsing = models.CharField(max_length=50, help_text='Статус парсинга',
                            verbose_name = 'Статус парсинга', default='Noparsing')

    class Meta:
        ordering = ['nomdobr']
        verbose_name = 'жалоба'
        verbose_name_plural = 'жалобы'

    def __str__(self):
        return self.nomdobr

    def get_absolute_url(self):
        return reverse("problem", args=(self.pk,))
