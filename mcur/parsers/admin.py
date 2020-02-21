from django.contrib import admin
from .models import (Parser)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'datecre', 'status',)
    list_display_links = ('uuid', 'name', 'datecre',)
    list_filter = ('status',)
