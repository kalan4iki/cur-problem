import django_tables2 as tables
from .models import Problem

class ProblemTable(tables.Table):
    class Meta:
        model = Problem
        # add class="paleblue" to <table> tag
        attrs = {'class': 'table table-bordered table-striped',
                'thead': {
                    'class': 'thead-light'
                }}
