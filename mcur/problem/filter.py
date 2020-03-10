import django_filters
from .models import Problem, Category, Status
from .tables import ProblemTable
from django_filters import ModelMultipleChoiceFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

def Categories(request):
    print(request)
    return Category.objects.all()

class ProblemFilter(django_filters.FilterSet):
    temat = ModelMultipleChoiceFilter(queryset=Category.objects.all())
    status = ModelMultipleChoiceFilter(queryset=Status.objects.all())

    class Meta:
        model = Problem
        fields = ['temat', 'status', 'statussys']
# def __init__(self, data=None, queryset=None, prefix=None, strict=None):
#     self.base_filters['temat'] = django_filters.filters.ModelMultipleChoiceFilter(
#         queryset=Category.objects.filter(problems__in=queryset).distinct(),
#     )
#     super().__init__(data, queryset, prefix, strict)

#    def __init__(self, request, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        temp = Category.objects.filter(problems__in=kwargs['queryset']).distinct()
#        print(temp)




class ProblemListView(SingleTableMixin, FilterView):
    table_class = ProblemTable
    model = Problem
    template_name = "template.html"
    filterset_class = ProblemFilter
