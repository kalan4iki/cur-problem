from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
# TODO: Модель ответов,
class Category(models.Model):
    name = models.CharField(max_length=255, help_text='Категория проблемы',
                            verbose_name = 'Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'категория проблемы'
        verbose_name_plural = 'категории проблем'

    def __str__(self):
        return self.name

class Podcategory(models.Model):
    name = models.CharField(max_length=255, help_text='Подкатегория проблемы',
                            verbose_name = 'Подкатегория')
    categ = models.ForeignKey(Category, on_delete=models.PROTECT, help_text='Категория проблемы',
                            verbose_name = 'Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'подкатегория проблемы'
        verbose_name_plural = 'подкатегории проблем'

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=100, help_text='Статус проблемы',
                            verbose_name = 'Статус')

    class Meta:
        ordering = ['name']
        verbose_name = 'статус проблемы'
        verbose_name_plural = 'статусы проблем'

    def __str__(self):
        return self.name

class Curator(models.Model):
    name = models.CharField(max_length=100, help_text='Куратор проблемы',
                            verbose_name = 'Куратор')

    class Meta:
        ordering = ['name']
        verbose_name = 'куратор проблемы'
        verbose_name_plural = 'кураторы проблем'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("curators", args=(self.pk,))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Curator, on_delete=models.PROTECT, verbose_name='Организация')
    post = models.CharField(max_length=100, help_text='Должность', verbose_name = 'Должность', default=' ', null=True, blank=True)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

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

class Problem(models.Model):
    pars = {
        ('0','На обновлении'),
        ('1','Обновлено'),
    }
    vis = {
        ('0','Не показывать'),
        ('1','Показывать'),
    }
    stat = {
        ('0','Закрыто'),
        ('1','В работе'),
        ('2','На модерации'),
    }
    nomdobr = models.CharField(max_length = 20, help_text = 'Номер проблемы',
                            verbose_name = 'Номер', unique = True)
    temat = models.ForeignKey(Category, on_delete=models.PROTECT, help_text='Тематика проблемы',
                            verbose_name = 'Тематика', blank=True, null=True)
    podcat = models.ForeignKey(Podcategory, on_delete=models.PROTECT, help_text='Подкатегория проблемы',
                            verbose_name = 'Подкатегория', blank=True, null=True)
    ciogv = models.ForeignKey(Minis, on_delete = models.PROTECT, blank=True,
                            help_text='ЦИОГВ', verbose_name = 'ЦИОГВ', null=True)
    text = models.TextField(help_text='Текст проблемы', verbose_name = 'Текст', blank=True, null=True)
    adres = models.CharField(max_length=255, help_text='Адрес проблемы',
                            verbose_name = 'Адрес', blank=True, null=True)
    url = models.URLField(help_text='URL проблемы', verbose_name = 'URL', blank=True, null=True)
    datecre = models.DateField(help_text='Дата создания', verbose_name = 'Дата создания', blank=True, null=True)
    dateotv = models.DateField(help_text='Дата ответа по доброделу', verbose_name = 'Дата ответа по доброделу', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, help_text='Статус в доброделе',
                            verbose_name = 'Статус в доброделе', blank=True, null=True)
    statussys = models.CharField(max_length=70, help_text='Статус проблемы',
                            verbose_name = 'Статус', default='2',choices=stat)
    parsing = models.CharField(max_length=50, help_text='Статус парсинга',
                            verbose_name = 'Статус парсинга', default='0', choices=pars)
    visible = models.CharField(max_length=50, help_text='Режим показа на сайте',
                            verbose_name = 'Режим', default='1', choices=vis)

    class Meta:
        ordering = ['nomdobr']
        verbose_name = 'жалоба'
        verbose_name_plural = 'жалобы'

    def __str__(self):
        return self.nomdobr

    def get_absolute_url(self):
        return reverse("problem", args=(self.nomdobr,))


class Term(models.Model):
    stats = {
        ('0','На исполнении'),
        ('1','На согласовании'),
        ('2','Исполнено'),
    }
    date = models.DateField(help_text='Срок', verbose_name = 'Срок', null=True)
    curat = models.ForeignKey(Curator, on_delete = models.PROTECT,
                            help_text='Куратор', verbose_name = 'Куратор')
    desck = models.TextField(help_text='Описание', verbose_name = 'Описание', blank=True, null=True)
    status = models.CharField(max_length=50, help_text= 'Статус ответа', verbose_name = 'Статус', default='0',choices=stats)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True,
                            verbose_name = 'Проблема', related_name='terms')
    anwr = models.BooleanField(default=False, verbose_name = 'Наличие ответа')

    class Meta:
        ordering = ['date']
        verbose_name = 'срок жалобы'
        verbose_name_plural = 'сроки жалоб'

    def __str__(self):
        temp = f'{self.curat} - {self.date.day}.{self.date.month}.{self.date.year}'
        return temp

    def get_absolute_url(self):
        return reverse("termview", args=(self.pk,))

class Answer(models.Model):
    stats = {
        ('0','На согласовании'),
        ('1','Утверждено'),
        ('2','Ответ отклонен')
    }
    text = models.TextField(help_text='Комментарий', verbose_name = 'Текст', null=True)
    datecre = models.DateField(auto_now_add=True, help_text='Дата создания', verbose_name = 'Дата создания', blank=True, null=True)
    datebzm = models.DateField(auto_now=True, help_text='Дата изменения', verbose_name = 'Дата изменения', blank=True, null=True)
    status = models.CharField(max_length=50, help_text= 'Статус ответа', verbose_name = 'Статус', default='0',choices=stats)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text='Кто дал ответ', verbose_name = 'Отвечающий')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, null=True, verbose_name = 'Назначение', related_name='answers')

    class Meta:
        ordering = ['pk']
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return f'{self.datecre.day}.{self.datecre.month}.{self.datecre.year}'
    #def __str__(self):
    def get_absolute_url(self):
        return reverse() # TODO: Доработать
    def get_status_display(self):
        return stats[self.status]

class Image(models.Model):
    otv = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, default=None, related_name='img', blank=True,
                            verbose_name='Ответ')
    file = models.ImageField(upload_to='photos', null=True, verbose_name = 'Фотография')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'
