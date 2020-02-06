from django.contrib import admin
from .models import Curator, Minis, Problem, Term, Access, Answer, UserProfile, Image
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image
    can_delete = False
    verbose_name_plural = 'Фотографии'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('nomobr', 'status', 'datecre', 'datebzm',)
    list_display_links = ('status', 'datecre', 'datebzm',)
    search_fields = ('status', 'datecre', 'datebzm',)
    inlines = (ImageInline,)

    def nomobr(self, answ):
        if answ.otvs.all().exists():
            if answ.otvs.all()[0].terms.all().exists():
                return answ.otvs.all()[0].terms.all()[0].nomdobr
            else:
                return 'Нет'
        else:
            return 'Нет'
    nomobr.short_description = "Номер жалобы"

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('nomdobr', 'temat', 'ciogv', 'text', 'adres', 'status', 'get_datecrok',)
    list_display_links = ('nomdobr', 'temat', 'ciogv', 'text', 'adres', 'status',)
    search_fields = ('nomdobr',)
    list_filter = ('ciogv__name', 'status', 'parsing')
    actions = ('pars',)

    def pars(self, request, queryset):
        for prob in queryset:
            prob.parsing = '0'
            prob.save()
        self.message_user(request, 'Действие выполнено')
    pars.short_description = 'Отправить на уточнение'

    def get_datecrok(self, obj):
        return "\n".join([f'({p.curat} - {p.date.day}.{p.date.month}.{p.date.year})  ' for p in obj.datecrok.all()])

@admin.register(Curator)
class CuratorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(Minis)
class MinisAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    #fiels = ('nomobr', 'date', 'curat', 'desck',)
    list_display = ('nomobr', 'date', 'curat', 'desck',)
    list_display_links = ('date', 'curat', 'desck',)
    search_fields = ('pk',)
    list_filter = ('curat__name', 'date',)

    def nomobr(self, srok):
        if srok.terms.all().exists():
            return srok.terms.all()[0].nomdobr
        else:
            return 'Нет'
    nomobr.short_description = "Номер жалобы"

    #nomobr.short_description = 'Номер жалобы'
    #exclude = ('day', 'month', 'year',)
    #actions = ('sootv',)

@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)
    search_fields = ('user',)

class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'

# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline, )

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

'''
    def procall(self, rec):
        return f'{round(((int(rec.complete) + int(rec.netreb)) * 100) / int(rec.allz))}'
    procall.short_description = 'Процент выполненого'
    def vrproc(self, rec):
        return f'{rec.vrabote}  ({rec.vraboteproc}%)'
    vrproc.short_description = 'В работе'
    def doproc(self, rec):
        return f'{rec.dost}  ({rec.dostproc}%)'
    doproc.short_description = 'Доступно'
    def coproc(self, rec):
        return f'{rec.complete}  ({rec.completeproc}%)'
    coproc.short_description = 'Выполнено'
    def neproc(self, rec):
        return f'{rec.netreb}  ({rec.netrebproc}%)'
    neproc.short_description = 'Не ребуются'

    def sootv(self, request, queryset):
        for rec in queryset:
            temp = rec.date.split('.')
            rec.day = temp[0]
            rec.month = temp[1]
            rec.year = temp[2]
            rec.save()
        self.message_user(request, 'Действие выполнено')
    sootv.short_description = 'Привести запись в соответсвие'
'''
