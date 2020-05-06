from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from mcur import settings
from .models import Problem

class Access:
    user = None
    request = None
    def __init__(self, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if self.user and self.request:
            self.authenticat()

    def authenticat(self):
        if not self.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))

    def problem(self, nomdobr):
        if Problem.objects.filter(nomdobr=nomdobr).exists():
            prob = Problem.objects.get(nomdobr=nomdobr)
        else:
            messages.error(self.request, 'Нет доступа к обращению.')
            return redirect('index')
        control = False
        if self.user.has_perm('problem.user_moderator'):
            control = True
        elif self.user.has_perm('problem.user_dispatcher'):
            if prob.terms.filter(Q(org=self.user.userprofile.org) | Q(curatuser=self.user)).exists():
                control = True
        elif self.user.has_perm('problem.user_executor'):
            if prob.terms.filter(Q(curat=self.user.userprofile.dep) | Q(curatuser=self.user) |
                                 Q(resolutions__curat=self.user.userprofile.dep) | Q(resolutions__curatuser=self.user)):
                control = True
        elif self.user.has_perm('problem.user_ty'):
            if prob.ciogv == self.user.userprofile.ty:
                control = True
        return control

    def api(self, uuid_user): #TODO доделать проверку api
        temp = ''