from django.contrib import admin
from .models import Curator, Minis, Problem, Term
# Register your models here.
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('nomdobr', 'temat', 'ciogv', 'text', 'adres', 'status', 'get_datecrok',)
    list_display_links = ('nomdobr', 'temat', 'ciogv', 'text', 'adres', 'status',)
    search_fields = ('date',)

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
    list_display = ('date', 'curat', 'desck',)
    list_display_links = ('date', 'curat', 'desck',)
    search_fields = ('date', 'curat', 'desck',)

    #exclude = ('day', 'month', 'year',)
    #actions = ('sootv',)

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
