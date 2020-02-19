import django_filters
from .models import Problem
from .tables import ProblemTable
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

class ProblemFilter(django_filters.FilterSet):
    #status = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Problem
        fields = ['temat', 'status', 'statussys']

class ProblemListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "template.html"

    filterset_class = ProblemFilter
