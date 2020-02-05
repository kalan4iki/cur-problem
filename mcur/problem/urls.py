from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import (api_problem, api_problem_detail, curator, prob, ProblemTableView,
                zaptable, add, termadd, delterm, lk, closedproblem, allproblem)
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mcur import settings
#Login = LoginView(template_name = 'problem/login.html')
#path('', index, name = 'index'),
urlpatterns = [
    path('test', ProblemTableView.as_view(), name='multitableview'),
    path('api/problem/', api_problem),
    path('api/problem/<int:np>', api_problem_detail),
    path('curators/<int:pk>', curator, name='curators'),
    path('problem/<int:pk>', prob, name='problem'),
    path('add/', add, name='add'),
    path('zap', zaptable),
    path('login/', LoginView.as_view(template_name = 'problem/login.html'), name='login'),
    #path('login/', CurLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('termadd/<int:pk>', termadd, name='termadd'),
    path('delterm/<int:pk>/<int:pkp>', delterm, name='termdel'),
    path('', lk, name='index'),
    path('', lk, name='lk'),
    path('closed/', closedproblem, name='closed'),
    path('allproblem/', allproblem, name='allproblem')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
