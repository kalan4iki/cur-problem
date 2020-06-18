from django.db import models
from problem.models import Person
# Create your models here.


class Appeal(models.Model):
    stats = {
        ('0', 'В работе'),
        ('1', 'На блокировке'),
        ('2', 'Закрыто'),
        ('3', 'Отклоненно')
    }
    nomdobr = models.CharField(max_length=20, help_text='Номер обращения', verbose_name='Номер')
    text = models.TextField(help_text='Комментарий', verbose_name='Текст', null=True, blank=True)
    datecre = models.DateField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания', blank=True,
                               null=True)
    datebzm = models.DateField(auto_now=True, help_text='Дата изменения', verbose_name='Дата изменения', blank=True,
                               null=True)
    status = models.CharField(max_length=50, help_text='Статус блокировки', verbose_name='Статус', default='0',
                              choices=stats)
    user = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, help_text='Кто направил на блокировку')

    class Meta:
        ordering = ['-datecre']
        verbose_name = 'блокировка'
        verbose_name_plural = 'блокировки'

    def __str__(self):
        return f'{self.nomdobr}'


class Result(models.Model):
    stats = {
        ('0', 'В работе'),
        ('1', 'На блокировке'),
        ('2', 'Закрыто'),
        ('3', 'Отклоненно')
    }
    block = models.ForeignKey(Appeal, on_delete=models.CASCADE, null=True, verbose_name='Обращение на блокировку')
    text = models.TextField(verbose_name='Текст', null=True, blank=True)
    chstatus = models.CharField(max_length=50, help_text='Статус блокировки', verbose_name='Статус', default='1',
                              choices=stats)
    nomkom = models.CharField(max_length=50, verbose_name='Номер комиссии', default=None, null=True, blank=True)
    datecre = models.DateTimeField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания',
                                   blank=True, null=True)
    user = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, help_text='Кто направил на блокировку')

    class Meta:
        ordering = ['datecre']
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return f'{self.block.nomdobr} {self.get_chstatus_display()}'


class Image(models.Model):
    otv = models.ForeignKey(Appeal, on_delete=models.CASCADE, null=True, default=None, related_name='imgs', blank=True,
                            verbose_name='Ответ')
    file = models.ImageField(upload_to='photos', null=True, verbose_name='Фотография')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'