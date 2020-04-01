from django.db import models
from problem.models import Problem, Person


class Message(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, verbose_name='Обращение',
                             related_name='chats')
    datecre = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    text = models.TextField(verbose_name='Текст', null=True)
    user = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, verbose_name='Автор')

    class Meta:
        ordering = ['datecre']
        verbose_name = 'сообщение по обращению'
        verbose_name_plural = 'сообщения по обращениям'

    def __str__(self):
        return f'{self.pk} - {self.user}'
