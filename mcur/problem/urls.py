from django.urls import path
from .views import index, api_problem, api_problem_detail, curator, prob


urlpatterns = [
    path('', index, name = 'index'),
    path('api/problem/', api_problem),
    path('api/problem/<int:np>', api_problem_detail),
    path('curators/<int:pk>', curator, name='curators'),
    path('problem/<int:np>', prob, name='problem'),
]
