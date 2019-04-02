from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from programdom.models import Problem


class EditProblemForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditProblemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))

    class Meta:
        model = Problem
        fields = ["title", "language"]
