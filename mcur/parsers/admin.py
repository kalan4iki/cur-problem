from django.contrib import admin
from .models import (Parser, Status, Action, ActionHistory, Loggings, Messages)
# Register your models here.
@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    list_display = ('name', 'datecre', 'status',)
    list_display_links = ('name', 'datecre',)
    list_filter = ('status__name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'nact',)
    list_display_links = ('name', 'nact',)

@admin.register(ActionHistory)
class ActionHistoryAdmin(admin.ModelAdmin):
    list_display = ('act', 'arg', 'status', 'lastaction', 'note')
    list_display_links = ('act', 'status', 'arg', 'lastaction', )
    actions = ('action',)
    list_filter = ('status',)

    def action(self, request, queryset):
        for prob in queryset:
            prob.status = '0'
            prob.save()
        self.message_user(request, 'Действие выполнено')
    action.short_description = 'Отправить на выполнение'


@admin.register(Loggings)
class LoggingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'note', 'datecre',)
    list_display_links = ('name', 'note', 'datecre',)
    list_filter = ('name', 'datecre',)

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('note', 'datecre',)
    list_display_links = ('note', 'datecre',)
    list_filter = ('note', 'datecre',)