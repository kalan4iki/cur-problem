from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('nomobr', 'user', 'datecre',)
    list_display_links = ('user', 'datecre',)

    def nomobr(self, mess):
        if mess.problem == None:
            return 'Нет'
        else:
            return mess.problem.nomdobr
    nomobr.short_description = "Номер жалобы"