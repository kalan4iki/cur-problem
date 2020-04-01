from django.urls import path
from.views import ChatProblem

urlpatterns = [
    path('api/chatproblem', ChatProblem, name='ChatProblem')
]