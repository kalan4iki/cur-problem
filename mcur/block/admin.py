from django.contrib import admin
from .models import Appeal, Image
# Register your models here.


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('nomdobr', 'text', 'status')
    list_display_links = ('nomdobr', 'text', 'status')
    search_fields = ('nomdobr',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('otv', 'file')
    list_display_links = ('otv', 'file')