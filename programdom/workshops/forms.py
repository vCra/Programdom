from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from programdom.models import WorkshopSession


class WorkshopsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkshopsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = WorkshopSession
        fields = ['title']


class WorkshopSessionEntryForm(forms.Form):

    code = forms.CharField(label="Session Code")

    def __init__(self, *args, **kwargs):
        super(WorkshopSessionEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    def clean_code(self):
        """
        Ensures that the code is active
        :return: code value if correct, else raise forms.ValidationError
        """

        cleaned_code = self.cleaned_data["code"]
        if not WorkshopSession.objects.filter(code__exact=cleaned_code).exists():
            raise forms.ValidationError("The code is incorrect!")
        return cleaned_code


class WorkshopProblemsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkshopProblemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = WorkshopSession
        fields = ['problems']