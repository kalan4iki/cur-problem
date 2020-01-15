from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, api_problem, api_problem_detail, curator, prob, ProblemTableView, zaptable, CurLogin, ELoginView, add, termadd, delterm

#Login = LoginView(template_name = 'problem/login.html')

urlpatterns = [
    path('', index, name = 'index'),
    path('test', ProblemTableView.as_view(), name='multitableview'),
    path('api/problem/', api_problem),
    path('api/problem/<int:np>', api_problem_detail),
    path('curators/<int:pk>', curator, name='curators'),
    path('problem/<int:pk>', prob, name='problem'),
    path('add/', add, name='add'),
    path('zap', zaptable),
    path('login/', CurLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('termadd/<int:pk>', termadd, name='termadd'),
    path('delterm/<int:pk>/<int:pkp>', delterm, name='termdel')
]
