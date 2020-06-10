from django.urls import path, include
from .views import main, table, obr_view, addresult, downimage, view_message, del_message

urlpatterns = [
    path('', main, name='blockindex'),
    path('table/', table, name='block_table'),
    path('obr_view/', obr_view, name='obr_view'),
    path('addresult/', addresult, name='addresult'),
    path('downimage/', downimage, name='downimage'),
    path('webpush/', include('webpush.urls')),
    path('view_message/', view_message, name='view_message'),
    path('del_message/', del_message, name='del_message')
]