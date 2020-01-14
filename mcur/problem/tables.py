import django_tables2 as tables
from django_tables2.views import MultiTableMixin
from django.views.generic.base import TemplateView
from .models import Problem, Term

class ProblemTable(tables.Table):
    nomdobr = tables.Column(linkify=True)
    #curat = tables.Column(linkify=True)
    #curat = tables.ManyToManyColumn(linkify_item=True)
    datecrok = tables.ManyToManyColumn(linkify_item=False)
    class Meta:
        model = Problem
        template_name = "django_tables2/bootstrap4.html"
        # add class="paleblue" to <table> tag
        attrs = {'class': 'table table-bordered table-striped',
                'thead': {
                    'class': 'thead-light'
                }}
        exclude = ("id", "text","url",)

class TermTable(tables.Table):
    class Meta:
        model = Term
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered table-striped',
                'thead': {
                    'class': 'thead-light'
                }}
