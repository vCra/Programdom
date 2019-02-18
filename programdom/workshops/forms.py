from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from programdom.models import Workshop


class WorkshopsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkshopsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = Workshop
        fields = ['title', 'start_time', 'end_time']