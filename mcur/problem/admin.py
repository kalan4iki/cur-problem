from django.contrib import admin
from .models import (Curator, Minis, Problem, Term, Access, Answer, UserProfile, Image, Category, Podcategory, Status,
                     Termhistory, Department, Author, DecisionProblem)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission
from django.contrib.admin.models import LogEntry
# Register your models here.


class ImageInline(admin.StackedInline):
    model = Image
    can_delete = False
    verbose_name_plural = 'Фотографии'


class AuthorInline(admin.TabularInline):
    model = Problem
    can_delete = False
    verbose_name_plural = 'Обращения'
    fields = ('nomdobr', 'temat', 'podcat')
    readonly_fields = ('nomdobr', 'temat', 'podcat')


class TermInline(admin.TabularInline):
    model = Term
    can_delete = False
    verbose_name_plural = 'Назначения'
    fields = ('pk', 'date', 'org', 'curat', 'curatuser')
    readonly_fields = ('pk', 'date', 'org', 'curat', 'curatuser')


class DecisionProblemAdmin(admin.TabularInline):
    model = DecisionProblem
    can_delete = False
    verbose_name_plural = 'Ход решения'
    fields = ('date', 'name', 'text')
    readonly_fields = ('date', 'name', 'text')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('fio', 'email', 'tel', 'problem_all')
    list_display_links = ('fio',)
    sortable_by = ('fio', 'email', 'tel', 'problem_all')
    search_fields = ('email', 'tel')
    inlines = (AuthorInline,)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'object_repr', 'change_message', 'user',)
    list_display_links = ('object_id',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Termhistory)
class TermhistoryAdmin(admin.ModelAdmin):
    list_display = ('text','datecre', 'user', )
    list_display_links = ('text',)
    list_filter = ('datecre', 'user',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'org')
    list_display_links = ('name',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('file',)
    list_display_links = ('file',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Podcategory)
class PodcategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('categ__name',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('status', 'datecre', 'datebzm',)
    list_display_links = ('status', 'datecre', 'datebzm',)
    search_fields = ('status', 'datecre', 'datebzm',)
    inlines = (ImageInline,)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('nomdobr', 'ciogv', 'text', 'adres', 'status', 'note',)
    list_display_links = ('nomdobr', 'ciogv', 'text', 'adres', 'status',)
    search_fields = ('nomdobr',)
    list_filter = ('visible', 'dateotv', 'status__name', 'note', 'temat', 'ciogv__name',)
    actions = ('pars', 'novisib', 'termnovisib', 'visib')
    inlines = (DecisionProblemAdmin, TermInline,)

    def pars(self, request, queryset):
        for prob in queryset:
            prob.parsing = '0'
            prob.save()
        self.message_user(request, 'Действие выполнено')
    pars.short_description = 'Отправить на уточнение'

    def novisib(self, request, queryset):
        queryset.update(visible='0')
        self.message_user(request, 'Действие выполнено')
    novisib.short_description = 'Убрать с сайта'

    def visib(self, request, queryset):
        queryset.update(visible='1')
        self.message_user(request, 'Действие выполнено')
    visib.short_description = 'Показать на сайте'

    def termnovisib(self, request, queryset):
        queryset.update(visible='2')
        self.message_user(request, 'Действие выполнено')
    termnovisib.short_description = 'Времмено убрать с сайта'


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
    list_display = ('nomobr', 'date', 'curat', 'desck',)
    list_display_links = ('date', 'curat', 'desck',)
    search_fields = ('pk',)
    list_filter = ('org__name', 'status', 'curat__name', 'date',)

    def nomobr(self, srok):
        if srok.problem == None:
            return 'Нет'
        else:
            return srok.problem.nomdobr

    nomobr.short_description = "Номер жалобы"


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)
    search_fields = ('user',)




class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ('org', 'dep', 'ty', 'post', 'uuid')
    readonly_fields = ('uuid',)
    verbose_name_plural = 'Доп. информация'


# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline, )

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
