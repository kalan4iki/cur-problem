from django.forms import modelform_factory, DecimalField, ModelForm, DateField, DateInput
from django.forms.widgets import Select
import datetime
from .models import Problem

class PrSet(ModelForm):
    class Meta:
        model = Problem
        fields= ('temat', 'ciogv', 'curat', 'text', 'adres', 'status', 'datecre', 'datecrok', 'dateotv')
        field_classes = {'datecre': DateField, 'datecrok': DateField, 'dateotv': DateField}
        widgets = {'datecre': DateInput(format='%d.%m.%Y'), 'datecrok': DateInput(), 'dateotv': DateInput()}
