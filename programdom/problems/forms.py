from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from programdom.models import Problem, ProblemTest


class EditProblemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditProblemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))

    class Meta:
        model = Problem
        fields = ["title", "language"]


class ProblemTestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProblemTestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))

    class Meta:
        model = ProblemTest
        fields = ['name', 'std_in', 'std_out']
        widgets = {
            "problem": forms.HiddenInput
        }
