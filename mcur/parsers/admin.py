from django.contrib import admin
from .models import (Parser, Status, Action, ActionHistory)
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
    list_display = ('act', 'arg', 'status', 'lastaction', )
    list_display_links = ('act', 'status', 'arg', 'lastaction', )