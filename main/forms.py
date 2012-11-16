#!/usr/bin/python
# -*- coding: utf-8 -*-
# from django.contrib.auth.forms import UserCreationForm
# from main.models import Schedule
from main.models import Event, NaturalClient

from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Fieldset
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
        exclude = ('owner', 'status', 'duration', )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'newEventForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            'description',
            Field('date', placeholder='DD/MM/AAAA'),
            'begin_time',
            Field('comments', rows="3"),
            HTML("<div class='control-group'><button type='button' class='btn btn-primary controls' data-toggle='collapse' data-target='#clientcase'>Asignar a un Cliente/Caso</button></div>"),
            Div('client',
                'case',
                css_class='collapse',
                css_id="clientcase"
            ),
            FormActions(
                Submit('add_event', u'Añadir'),
                Button('cancel', u'Cancelar'),
            )
        )


class NaturalClientForm(ModelForm):
    class Meta:
        model = NaturalClient
        exclude = ('owner', 'status', 'duration', )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'newEventForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            'description',
            Field('date', placeholder='DD/MM/AAAA'),
            'begin_time',
            Field('comments', rows="3"),
            HTML("<div class='control-group'><button type='button' class='btn btn-primary controls' data-toggle='collapse' data-target='#clientcase'>Asignar a un Cliente/Caso</button></div>"),
            Div('client',
                'case',
                css_class='collapse',
                css_id="clientcase"
            ),
            FormActions(
                Submit('add_event', u'Añadir'),
                Button('cancel', u'Cancelar'),
            )
        )
