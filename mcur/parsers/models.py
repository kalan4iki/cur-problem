from django.db import models
from problem.models import Problem


class Status(models.Model):
    name = models.CharField(max_length = 70, verbose_name = 'Название')

    class Meta:
        ordering = ['name']
        verbose_name = 'статус паресер'
        verbose_name_plural = 'статусы парсеров'

    def __str__(self):
        return self.name


class Parser(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.CharField(max_length = 40, verbose_name='Номер сессии', default=None, null=True)
    name = models.CharField(max_length = 40, help_text='Название парсера', verbose_name='Парсер')
    datecre = models.DateField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания', blank=True,
                               null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, help_text='Статус проблемы', verbose_name='Статус')

    class Meta:
        ordering = ['datecre']
        verbose_name = 'парсер'
        verbose_name_plural = 'парсеры'

    def __str__(self):
        return f'{self.name} №{self.id}'


class Action(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название действия')
    nact = models.CharField(max_length=40, verbose_name='Номер действия')

    class Meta:
        ordering = ['pk']
        verbose_name = 'действие'
        verbose_name_plural = 'действия'

    def __str__(self):
        return self.name


class ActionHistory(models.Model):
    stats = {
        ('0', 'На выполнении'),
        ('1', 'Выполнено'),
        ('2', 'Ошибка'),
    }
    act = models.ForeignKey(Action, on_delete=models.PROTECT, verbose_name='Действие', related_name='acts')
    pars = models.ForeignKey(Parser, on_delete=models.SET_NULL, verbose_name='Парсер', related_name='parsers',
                             blank=True, null=True)
    arg = models.CharField(max_length=50, verbose_name='Аргументы', default=None, null=True, blank=True)
    status = models.CharField(max_length=50, verbose_name='Статус', default='0', choices=stats)
    lastaction = models.DateTimeField(auto_now=True, verbose_name='Время выполнения', blank=True, null=True)
    note = models.CharField(max_length=100, verbose_name='Примечание', default=None, null=True, blank=True)

    class Meta:
        ordering = ['lastaction']
        verbose_name = 'история действия'
        verbose_name_plural = 'истории действий'


class Loggings(models.Model):
    stats = {
        ('0', 'Добавлено'),
        ('1', 'Обновлено'),
        ('2', 'Прочее'),
    }
    name = models.CharField(max_length=50, verbose_name='Статус', default='0', choices=stats)
    note = models.CharField(max_length=255, verbose_name='Примечание', default=None, blank=True)
    datecre = models.DateField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания', blank=True,
                               null=True)

    class Meta:
        ordering = ['pk']
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

    def __str__(self):
        return f'{self.note} - {self.name}'


class Logpars(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name='Проблема', related_name='logpars', blank=True, null=True)
    datecre = models.DateTimeField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания', blank=True,
                               null=True)

    class Meta:
        ordering = ['datecre']
        verbose_name = 'история парсера'
        verbose_name_plural = 'истории парсера'

    def __str__(self):
        return f'{self.problem.nomdobr} - {self.datecre.strftime("%d.%m.%Y %H:%M:%S")}'


class Logspars(models.Model):
    names = {
        ('0', 'Изменение тематики'),
        ('1', 'Изменение подкатегории'),
        ('2', 'Добавление автора'),
        ('3', 'Обновление даты ответа'),
        ('4', 'Обновление статуса'),
    }
    oper = models.ForeignKey(Logpars, on_delete=models.CASCADE, verbose_name='Операция', related_name='logspars', blank=True, null=True)
    name = models.CharField(verbose_name='Название операции', max_length=255, default='0', choices=names, null=True)
    lastval = models.CharField(verbose_name='Предыдущее значение', max_length=255, default=None, null=True)
    newval = models.CharField(verbose_name='Новое значение', max_length=255, default=None, null=True)

    class Meta:
        ordering = ['pk']
        verbose_name = 'история парсера'
        verbose_name_plural = 'истории парсера'

    def __str__(self):
        return self.name

class Messages(models.Model):
    note = models.TextField(verbose_name='Ошибка', default=None, blank=True)
    act = models.ForeignKey(ActionHistory, on_delete=models.CASCADE, verbose_name='Действие', default=None)
    datecre = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)

    class Meta:
        ordering = ['pk']
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Problem)
def logproblem(sender, instance, **kwargs):
    new = instance
    if Problem.objects.filter(nomdobr=new.nomdobr).exists():
        last = Problem.objects.get(nomdobr=new.nomdobr)
        b = Logpars(problem=last)
        b.save()
        a = None
        if new.temat != last.temat:
            a = Logspars(oper=b, name='0', lastval=last.temat.name, newval=new.temat.name)
            a.save()
        if new.podcat != last.podcat:
            a = Logspars(oper=b, name='1', lastval=last.podcat.name, newval=new.podcat.name)
            a.save()
        if new.author != last.author:
            if last.author == None:
                a = Logspars(oper=b, name='2', lastval=None, newval=new.author.email)
                a.save()
        if new.dateotv != last.dateotv:
            a = Logspars(oper=b, name='3', lastval=last.dateotv.strftime('%d.%m.%Y'), newval=new.dateotv.strftime('%d.%m.%Y'))
            a.save()
        if new.status != last.status:
            a = Logspars(oper=b, name='4', lastval=last.status.name, newval=new.status.name)
        if a != None:
            a.save()
        else:
            b.delete()
