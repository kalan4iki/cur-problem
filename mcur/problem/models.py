from django.db import models

# Create your models here.

class Curator(models.Model):
    name = models.CharField(max_length=40, help_text='Куратор проблемы',
                            verbose_name = 'Куратор')

    class Meta:
        ordering = ['name']
        verbose_name = 'куратор проблемы'
        verbose_name_plural = 'кураторы проблем'

    def __str__(self):
        return self.name

class Minis(models.Model):
    name = models.CharField(max_length=40, help_text='ЦИОГВ',
                            verbose_name = 'ЦИОГВ')

    class Meta:
        ordering = ['name']
        verbose_name = 'ЦИОГВ'
        verbose_name_plural = 'ЦИОГВ'

    def __str__(self):
        return self.name

class Problem(models.Model):
    nomdobr = models.CharField(max_length=20, help_text='Номер проблемы',
                            verbose_name = 'Номер')
    temat = models.CharField(max_length=20, help_text='Тематика проблемы',
                            verbose_name = 'Тематика', blank=True, null=True)
    ciogv = models.ForeignKey(Minis, on_delete = models.PROTECT, blank=True,
                            help_text='ЦИОГВ', verbose_name = 'ЦИОГВ', null=True)
    curat = models.ForeignKey(Curator, on_delete = models.PROTECT, blank=True,
                            help_text='Куратор', verbose_name = 'Куратор', null=True)
    text = models.TextField(help_text='Текст проблемы', verbose_name = 'Текст', blank=True, null=True)
    adres = models.CharField(max_length=255, help_text='Адрес проблемы',
                            verbose_name = 'Адрес', blank=True, null=True)
    url = models.URLField(help_text='URL проблемы', verbose_name = 'URL', blank=True, null=True)
    datecre = models.DateField(help_text='Дата создания', verbose_name = 'Дата создания', blank=True, null=True)
    datecrok = models.DateField(help_text='Срок задачи', verbose_name = 'Срок задачи', blank=True, null=True)
    dateotv = models.DateField(help_text='Дата ответа исполнителя', verbose_name = 'Дата ответа исполнителя', blank=True, null=True)
    status = models.CharField(max_length=50, help_text='Статус проблемы',
                            verbose_name = 'Статус', blank=True, null=True)
    class Meta:
        ordering = ['nomdobr']
        verbose_name = 'жалоба'
        verbose_name_plural = 'жалобы'

    def __str__(self):
        return self.nomdobr
