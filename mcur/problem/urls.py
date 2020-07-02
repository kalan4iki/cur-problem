from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (api_problem, api_problem_detail, api_answer_detail, prob, addanswer,
                    zaptable, add, lk, search, Answer_approve,
                    Answer_modify, development, resolutionadd, zapros,
                    createuser, dashboard, export_pdf, statandact, api_action,
                    listuser, apis, dopaction, analysis, problems)
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from mcur import settings

urlpatterns = [
    url(r'^$', lk, name='lk'),
    url(r'createuser/', createuser, name='createuser'),
    path('api/problem/', api_problem),
    path('api/problem/<int:np>', api_problem_detail),
    path('api/answer/', api_answer_detail),
    path('api/action/', api_action, name='api_action'),
    path('api/', apis, name='api'),
    path('problem/<int:pk>', prob, name='problem'),
    path('add/', add, name='add'),
    path('zap', zaptable),
    path('login/', LoginView.as_view(template_name = 'problem/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('resolution/<int:pk>', resolutionadd, name='resolutionadd'),
    path('index/', lk, name='index'),
    path('problems/<str:action>', problems, name='problems'),
    path('search/', search, name='search'),
    path('addanswer/<int:pk>', addanswer, name='addanswer'),
    path('answer/action/aprrove/<int:pk>', Answer_approve, name='answer_approve'),
    path('answer/action/modify/<int:pk>', Answer_modify, name='answer_modify'),
    path('calendary/', development, name='calendary'),
    path('dashboard/', dashboard, name='dashboard'),
    path('listuser/', listuser, name='listuser'),
    path('export_pdf/<int:pk>', export_pdf, name= 'export_pdf'),
    path('statandact/', statandact, name='statandact'),
    path('api/dopaction', dopaction, name='dopaction'),
    path('zapros/', zapros, name='zapros'),
    path('analysis/', analysis, name='analysis'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
