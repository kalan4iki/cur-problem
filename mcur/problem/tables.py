import django_tables2 as tables
from django.contrib.auth.models import User
from django_tables2.views import MultiTableMixin
from django.views.generic.base import TemplateView
from .models import Problem, Term, Person
from parsers.models import Parser, ActionHistory

class ProblemTable(tables.Table):
    nomdobr = tables.Column(verbose_name='Номер добродел', linkify=True)
    class Meta:
        model = Problem
        template_name = "django_tables2/bootstrap4.html"
        # add class="paleblue" to <table> tag
        attrs = {'class': 'table table-bordered table-striped table-head-fixed ',
                'thead': {
                    'class': 'thead-light'
                }}
        fields = ('nomdobr', 'dateotv', 'temat', 'podcat', 'status', 'statussys', 'datecre')
        exclude = ("id", "text","url","parsing", "visible")

class TermTable(tables.Table):
    class Meta:
        model = Term
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-striped',
                'thead': {
                    'class': 'thead-light'
                }}

class ParsTable(tables.Table):
    class Meta:
        model = Parser
        template_name = "django_tables2/bootstrap4.html"

class HistTable(tables.Table):
    class Meta:
        model = ActionHistory
        template_name = "django_tables2/bootstrap4.html"
        exclude = ("pars",)

class UserTable(tables.Table):
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        exclude = ("password", "is_active", "is_staff", "is_superuser",)