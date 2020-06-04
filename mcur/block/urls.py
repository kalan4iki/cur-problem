from django.urls import path, include
from .views import main, table, obr_view, addresult, downimage

urlpatterns = [
    path('', main, name='blockindex'),
    path('table/', table, name='block_table'),
    path('obr_view/', obr_view, name='obr_view'),
    path('addresult/', addresult, name='addresult'),
    path('downimage/', downimage, name='downimage'),
    path('webpush/', include('webpush.urls')),
]