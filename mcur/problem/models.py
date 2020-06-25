from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.db.models import F
import uuid


class Person(User):

    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=255, help_text='Категория проблемы',
                            verbose_name='Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'категория проблемы'
        verbose_name_plural = 'категории проблем'

    def __str__(self):
        return self.name


class Podcategory(models.Model):
    name = models.CharField(max_length=400, help_text='Подкатегория проблемы',
                            verbose_name='Подкатегория')
    categ = models.ForeignKey(Category, on_delete=models.PROTECT, help_text='Категория проблемы',
                              verbose_name='Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'подкатегория проблемы'
        verbose_name_plural = 'подкатегории проблем'

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, help_text='Статус проблемы',
                            verbose_name='Статус')

    class Meta:
        ordering = ['name']
        verbose_name = 'статус проблемы'
        verbose_name_plural = 'статусы проблем'

    def __str__(self):
        return self.name


class Curator(models.Model):
    name = models.CharField(max_length=100, help_text='Куратор проблемы', verbose_name='Организация')

    class Meta:
        ordering = ['name']
        verbose_name = 'организация'
        verbose_name_plural = 'организации'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("curators", args=(self.pk,))


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Отдел')
    org = models.ForeignKey(Curator, on_delete=models.CASCADE, verbose_name='Организация', related_name='departments')

    class Meta:
        ordering = ['name']
        verbose_name = 'отдел'
        verbose_name_plural = 'отделы'

    def __str__(self):
        return f'{self.org.name}, {self.name}'


class Minis(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        ordering = ['pk']
        verbose_name = 'территориальное уравление'
        verbose_name_plural = 'территориальные уравления'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Curator, on_delete=models.SET_NULL, verbose_name='Организация', null=True)
    dep = models.ForeignKey(Department, on_delete=models.SET_NULL, verbose_name='Отдел', default=None, null=True,
                            blank=True)
    ty = models.ForeignKey(Minis, on_delete=models.SET_NULL, verbose_name='Тер. управление', default=None, null=True,
                            blank=True)
    post = models.CharField(max_length=100, help_text='Должность', verbose_name='Должность', default=' ', null=True,
                            blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Токен')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


class Access(models.Model):
    lvls = {
        ('r', 'Чтение'),
        ('w', 'Запись'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    dost = models.ManyToManyField(Curator, verbose_name='Организация')
    lvl = models.CharField(max_length=40, help_text='Уровень доступа', verbose_name='Уровень доступа',
                           choices=lvls)

    class Meta:
        ordering = ['user']
        verbose_name = 'доступ'
        verbose_name_plural = 'доступы'
        # permissions = {"", }

    def __str__(self):
        return self.user


class Author(models.Model):
    fio = models.CharField(max_length=250, help_text='ФИО заявителя', verbose_name='ФИО', blank=True, null=True)
    email = models.EmailField(help_text='Почта заявителя', verbose_name='Почта', blank=True, null=True)
    tel = models.CharField(max_length=50, help_text='Телефон заявителя', verbose_name='Телефон', blank=True, null=True)

    class Meta:
        ordering = ['email']
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

    def __str__(self):
        return f'{self.fio} - {self.email}'

    def problem_all(self):
        return len(self.problems.all())


class Problem(models.Model):
    pars = {
        ('0', 'На обновлении'),
        ('1', 'Обновлено'),
    }
    vis = {
        ('0', 'Не показывать'),
        ('1', 'Показывать'),
        ('2', 'Временно скрыто'),
    }
    stat = {
        ('0', 'Закрыто'),
        ('1', 'В работе'),
        ('2', 'На модерации'),
    }
    nomdobr = models.CharField(max_length=20, help_text='Номер обращения', verbose_name='Номер', unique=True)
    temat = models.ForeignKey(Category, on_delete=models.PROTECT, help_text='Тематика проблемы',
                              verbose_name='Тематика', blank=True, null=True, related_name='problems')
    podcat = models.ForeignKey(Podcategory, on_delete=models.PROTECT, help_text='Подкатегория проблемы',
                               verbose_name='Подкатегория', blank=True, null=True, related_name='problems')
    ciogv = models.ForeignKey(Minis, on_delete=models.PROTECT, blank=True, verbose_name='Тер. управление', default=None,
                              null=True, related_name='problems')
    text = models.TextField(help_text='Текст проблемы', verbose_name='Текст', blank=True, null=True)
    adres = models.CharField(max_length=255, help_text='Адрес проблемы', verbose_name='Адрес', blank=True, null=True)
    url = models.URLField(help_text='URL проблемы', verbose_name='URL', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, default=None, blank=True,
                               verbose_name='Автор обращения', related_name='problems')
    datecre = models.DateField(help_text='Дата создания', verbose_name='Дата создания', blank=True, null=True)
    dateotv = models.DateField(help_text='Дата ответа по доброделу', verbose_name='Дата ответа по доброделу',
                               blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, help_text='Статус в доброделе',
                               verbose_name='Статус в доброделе', blank=True, null=True, related_name='problems')
    statussys = models.CharField(max_length=70, help_text='Статус проблемы',
                                 verbose_name='Статус', default='2', choices=stat)
    parsing = models.CharField(max_length=50, help_text='Статус парсинга',
                               verbose_name='Статус парсинга', default='0', choices=pars)
    visible = models.CharField(max_length=50, help_text='Режим показа на сайте',
                               verbose_name='Режим', default='1', choices=vis)
    note = models.CharField(max_length=255, verbose_name='Замечание', default=None, null=True, blank=True)

    class Meta:
        ordering = ['dateotv']
        verbose_name = 'обращение'
        verbose_name_plural = 'обращения'

    def __str__(self):
        return self.nomdobr

    def get_absolute_url(self):
        return reverse("problem", args=(self.nomdobr,))


class Term(models.Model):
    stats = {
        ('0', 'На исполнении'),
        ('1', 'На согласовании'),
        ('2', 'Исполнено'),
    }
    datecre = models.DateField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания', blank=True,
                               null=True)
    date = models.DateField(help_text='Срок', verbose_name='Срок', null=True)
    org = models.ForeignKey(Curator, on_delete=models.SET_NULL, verbose_name='Организация', blank=True, null=True,
                            related_name='terms')
    curat = models.ForeignKey(Department, on_delete=models.SET_NULL, verbose_name='Отдел', blank=True, null=True,
                              related_name='terms')
    curatuser = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='curatuser',
                                  verbose_name='Сотрудник', blank=True, null=True)
    desck = models.TextField(help_text='Описание', verbose_name='Описание', blank=True, null=True)
    status = models.CharField(max_length=50, help_text='Статус ответа', verbose_name='Статус', default='0',
                              choices=stats)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, verbose_name='Проблема',
                                related_name='terms')
    anwr = models.BooleanField(default=False, verbose_name='Наличие ответа')
    user = models.ForeignKey(Person, on_delete=models.SET_NULL, default=None, null=True)
    further = models.BooleanField(verbose_name='Для дальнейшего рассмотрения', default=False)
    furtherdate = models.DateField(verbose_name='Срок обещания', default=None, null=True, blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'назначение'
        verbose_name_plural = 'назначения'

    def __str__(self):
        temp = f'{self.curat} - {self.date.day}.{self.date.month}.{self.date.year}'
        return temp

    def get_absolute_url(self):
        return reverse('problem', kwargs={'pk': self.problem.nomdobr})

    def on_close(self):
        if self.status == '0':
            return False
        else:
            return True

class Termhistory(models.Model):
    text = models.TextField(help_text='Текст резолюции', verbose_name='Описание', null=True)
    datecre = models.DateField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания', blank=True,
                               null=True)
    curat = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='curaters',
                              verbose_name='Отдел', blank=True, null=True)
    curatuser = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='curatuserterm',
                                  verbose_name='Сотрудник', blank=True, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, default=None, null=True, related_name='resolutions')
    user = models.ForeignKey(Person, on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        ordering = ['user']
        verbose_name = 'резолюция'
        verbose_name_plural = 'резолюции'


class Answer(models.Model):
    stats = {
        ('0', 'На согласовании'),
        ('1', 'Утверждено'),
        ('2', 'Ответ отклонен')
    }
    text = models.TextField(help_text='Комментарий', verbose_name='Текст', null=True)
    datecre = models.DateField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания', blank=True,
                               null=True)
    datebzm = models.DateField(auto_now=True, help_text='Дата изменения', verbose_name='Дата изменения', blank=True,
                               null=True)
    status = models.CharField(max_length=50, help_text='Статус ответа', verbose_name='Статус', default='0',
                              choices=stats)
    user = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, help_text='Кто дал ответ',
                             verbose_name='Отвечающий')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, null=True, verbose_name='Назначение',
                             related_name='answers')

    class Meta:
        ordering = ['pk']
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return f'{self.datecre.day}.{self.datecre.month}.{self.datecre.year}'


class Image(models.Model):
    otv = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, default=None, related_name='imgs', blank=True,
                            verbose_name='Ответ')
    prob = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, default=None, related_name='imgs', blank=True,
                            verbose_name='Фотография проблемы')
    file = models.ImageField(upload_to='photos', null=True, verbose_name='Фотография')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'


class EditProblem(models.Model):
    datecre = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    prob = models.ForeignKey(Problem, verbose_name='Обращение', on_delete=models.CASCADE, null=True, default=None,
                             related_name='editprob')

    def __str__(self):
        return f'Изменение от {self.datecre} обращение №{self.prob.nomdobr}'

    class Meta:
        ordering = ['-datecre']
        verbose_name = 'изменение обращения'
        verbose_name_plural = 'изменения обращений'


class Editable(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название', null=True, default=None)
    lastval = models.TextField(verbose_name='Старое значение', null=True, default=None)
    newval = models.TextField(verbose_name='Новое значение', null=True, default=None)
    operation = models.ForeignKey(EditProblem, verbose_name='Операция изменения', on_delete=models.CASCADE, null=True,
                                  default=None, related_name='editable')

    class Meta:
        ordering = ['-pk']


class DecisionProblem(models.Model):
    prob = models.ForeignKey(Problem, verbose_name='Обращение', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата создания')
    name = models.CharField(max_length=255, verbose_name='Имя')
    text = models.TextField(verbose_name='Текст', null=True, default=None)

    def __str__(self):
        return f'Решине от {self.name} обращения {self.prob.nomdobr}'

    class Meta:
        ordering = ['-date']
        verbose_name = 'ход решения'
        verbose_name_plural = 'ходы решения'


class Images(models.Model):
    prob = models.ForeignKey(Problem, verbose_name='Обращение', on_delete=models.CASCADE, null=True, default=None,
                             blank=True)
    decis = models.ForeignKey(DecisionProblem, verbose_name='Ход решения', on_delete=models.CASCADE, null=True,
                              default=None, blank=True)
    url = models.CharField(max_length=300, verbose_name='URL изображения')

    class Meta:
        ordering = ['-pk']
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
