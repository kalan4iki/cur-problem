from django.contrib import admin
from .models import (Curator, Minis, Problem, Term, Access, Answer, UserProfile, Image, Category, Podcategory, Status,
                     Termhistory, Department)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission

# Register your models here.


class ImageInline(admin.StackedInline):
    model = Image
    can_delete = False
    verbose_name_plural = 'Фотографии'


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

    def pars(self, request, queryset):
        for prob in queryset:
            prob.parsing = '0'
            prob.save()
        self.message_user(request, 'Действие выполнено')
    pars.short_description = 'Отправить на уточнение'

    def novisib(self, request, queryset):
        for prob in queryset:
            prob.visible = '0'
            prob.save()
        self.message_user(request, 'Действие выполнено')
    novisib.short_description = 'Убрать с сайта'

    def visib(self, request, queryset):
        for prob in queryset:
            prob.visible = '1'
            prob.save()
        self.message_user(request, 'Действие выполнено')
    visib.short_description = 'Показать на сайте'

    def termnovisib(self, request, queryset):
        for prob in queryset:
            prob.visible = '2'
            prob.save()
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
    verbose_name_plural = 'Доп. информация'


# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline, )

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
