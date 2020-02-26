from django.forms import (modelform_factory, DecimalField, ModelForm, DateField, Form,
                        DateInput, TextInput, ModelChoiceField, ImageField, Textarea, CharField)
from django.contrib.auth import authenticate, get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.utils.text import capfirst
from django import forms
from django.forms.widgets import Select
import datetime
from .models import Problem, Term, Answer, Termhistory, Department

class ResolutionForm(ModelForm):
    curat = ModelChoiceField(queryset=Department.objects.all(), label='Отдел')
    curatuser = ModelChoiceField(queryset=User.objects.all(), label='Сотрудник')
    class Meta:
        model = Termhistory
        fields = ('text',)
        TA = Textarea
        TA.template_name="widgets/textarea.html"
        widgets = {'text': TA}

    def __init__(self, curat_qs=None, curatuser_qs=None, **kwargs):
        super(ResolutionForm, self).__init__(**kwargs)
        self.helper = FormHelper()
        if curat_qs:
            self.fields['curat'].queryset = curat_qs
        if curatuser_qs:
            self.fields['curatuser'].queryset = curatuser_qs
        #self.fields['curatuser'].queryset = kwargs.pop('curatuser_qs')

class AnswerForm(Form):
    text = CharField(label=u'Комментарий')
    image = ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

class TermForm(ModelForm):
    class Meta:
        model = Term
        fields = {'date', 'desck','org', 'curat', 'curatuser'}
        TA = Textarea
        TA.template_name="widgets/textarea.html"
        widgets = {'desck': TA}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()

class PrAdd(ModelForm):
    class Meta:
        model = Problem
        fields = {'nomdobr'}

class PrSet(ModelForm):
    class Meta:
        model = Problem
        fields= ('temat', 'ciogv', 'text', 'adres', 'status', 'datecre', 'dateotv')
        field_classes = {'datecre': DateField, 'dateotv': DateField}
        widgets = {'datecre': DateInput(format='%d.%m.%Y'), 'dateotv': DateInput()}

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': ("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-signin'
        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
