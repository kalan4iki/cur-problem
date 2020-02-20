from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import (api_problem, api_problem_detail, prob, addanswer, ProblemNoListView,
                zaptable, add, termadd, delterm, lk, closedproblem, search, ProblemListView,
                ProblemPodxListView, ProblemProsrListView, termview, exportxls, AnswerAction)
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from mcur import settings
#Login = LoginView(template_name = 'problem/login.html')
#path('', index, name = 'index'),
urlpatterns = [
    url(r'^$', lk, name='lk'),
    path('api/problem/', api_problem),
    path('api/problem/<int:np>', api_problem_detail),
    path('problem/<int:pk>', prob, name='problem'),
    path('add/', add, name='add'),
    path('zap', zaptable),
    path('login/', LoginView.as_view(template_name = 'problem/login.html'), name='login'),
    #path('login/', CurLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('termadd/<int:pk>', termadd, name='termadd'),
    path('delterm/<int:pk>/<int:pkp>', delterm, name='termdel'),
    path('index/', lk, name='index'),
    path('search/', search, name='search'),
    path('addanswer/<int:pk>', addanswer, name='addanswer'),
    url(r'allproblem/', ProblemListView.as_view(), name='allproblem'),
    url(r'noproblem/', ProblemNoListView.as_view(), name='noproblem'),
    url(r'podxproblem/', ProblemPodxListView.as_view(), name='podxproblem'),
    url(r'prosrproblem/', ProblemProsrListView.as_view(), name='prosrproblem'),
    url(r'^export/xls/$', exportxls, name='exportxls'),
    path('term/<int:pk>', termview, name='termview'),
    url(r'answer/action/aprrove/<int:pk>', AnswerAction.Approve, name='term_approve'),
    path('answer/action/modify/<int:pk>', AnswerAction.Modify, name='term_modify'),
]
#    path('allproblem/', allproblem, name='allproblem'),

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
handler = 'views.custom404'
