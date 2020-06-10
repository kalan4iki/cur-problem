from django.contrib import admin
from .models import Appeal, Image, Result
# Register your models here.

class ResultInline(admin.StackedInline):
    model = Result
    can_delete = True
    verbose_name_plural = 'Смена статуса'


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('nomdobr', 'text', 'status')
    list_display_links = ('nomdobr', 'text', 'status')
    search_fields = ('nomdobr',)
    inlines = (ResultInline,)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('otv', 'file')
    list_display_links = ('otv', 'file')