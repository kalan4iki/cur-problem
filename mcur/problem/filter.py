import django_filters
from .models import Problem, Category, Status
from .tables import ProblemTable
from django_filters import ModelMultipleChoiceFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

class ProblemFilter(django_filters.FilterSet):
    temat = ModelMultipleChoiceFilter(queryset=Category.objects.all())
    status = ModelMultipleChoiceFilter(queryset=Status.objects.all())

    class Meta:
        model = Problem
        fields = ['temat', 'status', 'statussys']




class ProblemListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "template.html"
    filterset_class = ProblemFilter
