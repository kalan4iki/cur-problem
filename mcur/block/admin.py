from django.contrib import admin
from .models import Appeal, Image, Result
# Register your models here.

class ResultInline(admin.StackedInline):
    model = Result
    can_delete = False
    verbose_name_plural = 'Смена статуса'
    fields = ('text', 'chstatus', 'nomkom', 'datecre', 'user')
    readonly_fields = ('datecre',)


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('nomdobr', 'text', 'status', 'datecre')
    list_display_links = ('nomdobr', 'text', 'status')
    search_fields = ('nomdobr',)
    list_filter = ('status', 'datecre')
    inlines = (ResultInline,)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('otv', 'file')
    list_display_links = ('otv', 'file')
