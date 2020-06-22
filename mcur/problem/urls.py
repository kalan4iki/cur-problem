from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (api_problem, api_problem_detail, api_answer_detail, prob, addanswer, ProblemNoListView, addparsing,
                    zaptable, add, termadd, delterm, lk, closedproblem, search, ProblemListView, ProblemPodxListView,
                    ProblemProsrListView, exportxls, Answer_approve, Answer_modify, development, resolutionadd, zapros,
                    createuser, dashboard, ProblemTodayListView, ProblemMeListView, export_pdf, statandact, api_action,
                    listuser, term_approve, api_report, addty, ProblemTyListView, apis, dopaction, ProblemOrgView,
                    ProblemFuListView, delty, changeterm, analysis)
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
    path('api/report/', api_report, name='api_report'),
    path('api/', apis, name='api'),
    path('problem/<int:pk>', prob, name='problem'),
    path('add/', add, name='add'),
    path('zap', zaptable),
    path('login/', LoginView.as_view(template_name = 'problem/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('termadd/<int:pk>', termadd, name='termadd'),
    path('resolution/<int:pk>', resolutionadd, name='resolutionadd'),
    path('delterm/<int:pk>', delterm, name='termdel'),
    path('index/', lk, name='index'),
    path('search/', search, name='search'),
    path('addanswer/<int:pk>', addanswer, name='addanswer'),
    path('closed/', closedproblem, name='closed'),
    url(r'allproblem/', ProblemListView.as_view(), name='allproblem'),
    url(r'noproblem/', ProblemNoListView.as_view(), name='noproblem'),
    url(r'podxproblem/', ProblemPodxListView.as_view(), name='podxproblem'),
    url(r'prosrproblem/', ProblemProsrListView.as_view(), name='prosrproblem'),
    url(r'todayproblem/', ProblemTodayListView.as_view(), name='todayproblem'),
    url(r'meproblem/', ProblemMeListView.as_view(), name='meproblem'),
    url(r'typroblem/', ProblemTyListView.as_view(), name='typroblem'),
    url(r'orgproblem/', ProblemOrgView, name='orgproblem'),
    url(r'^export/xls/$', exportxls, name='exportxls'),
    url(r'fuproblem/', ProblemFuListView.as_view(), name='fuproblem'),
    path('answer/action/aprrove/<int:pk>', Answer_approve, name='answer_approve'),
    path('answer/action/modify/<int:pk>', Answer_modify, name='answer_modify'),
    path('calendary/', development, name='calendary'),
    path('dashboard/', dashboard, name='dashboard'),
    path('listuser/', listuser, name='listuser'),
    path('addparsing/<int:pk>', addparsing, name='addparsing'),
    path('export_pdf/<int:pk>', export_pdf, name= 'export_pdf'),
    path('statandact/', statandact, name='statandact'),
    path('term_approve/<int:pk>', term_approve, name='term_approve'),
    path('addty/', addty, name='addty'),
    path('api/dopaction', dopaction, name='dopaction'),
    path('zapros/', zapros, name='zapros'),
    path('changeterm/', changeterm, name='changeterm'),
    path('analysis/', analysis, name='analysis'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
