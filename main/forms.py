# from django.contrib.auth.forms import UserCreationForm
# from main.models import Schedule
from main.models import Event

from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
# class UserForm(UserCreationForm):
#     firm = forms.CharField(required=True)

#     def save(self, commit=False):
#         user = super(UserForm, self).save(commit=False)
#         user.save()

#         try:
#             profile = user.get_profile()
#         except:
#             profile = UserProfile(user=user)

#         schedule = Schedule()
#         schedule.save()

#         profile.firm = self.cleaned_data['firm']

#         profile.ownSchedule = schedule
#         profile.save()

#         return user


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('owner', 'status', 'result', )
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'description',
        'case',
        'date',
        'begin_time',
        'end_time',
        Field('comments', rows="3"),
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )
