from django.urls import path
from django.contrib.auth.views import LoginView
from .views import index, api_problem, api_problem_detail, curator, prob, ProblemTableView, zaptable
from .forms import AuthenticationForm
#Login = LoginView(template_name = 'problem/login.html')

urlpatterns = [
    path('', index, name = 'index'),
    path('test', ProblemTableView.as_view(), name='multitableview'),
    path('api/problem/', api_problem),
    path('api/problem/<int:np>', api_problem_detail),
    path('curators/<int:pk>', curator, name='curators'),
    path('problem/<int:pk>', prob, name='problem'),
    path('zap', zaptable),
    path('login', LoginView.as_view(template_name = 'problem/login.html', authentication_form=AuthenticationForm), name='login')
]
