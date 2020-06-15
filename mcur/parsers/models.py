from django.db import models


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

class Messages(models.Model):
    note = models.TextField(verbose_name='Ошибка', default=None, blank=True)
    act = models.ForeignKey(ActionHistory, on_delete=models.CASCADE, verbose_name='Действие', default=None)
    datecre = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)

    class Meta:
        ordering = ['pk']
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'