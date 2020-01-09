from django.forms import modelform_factory, DecimalField
from django.forms.widgets import Select

from .models import Problem

PrForm = modelform_factory(Problem, field={'nomdobr'},)
