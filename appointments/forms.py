#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class DynamicChoiceField(forms.ChoiceField):
    def validate(self, value):
        if not value:
            raise ValidationError(self.error_messages['invalid_choice'] % {'value': value})


class IdForm (forms.Form):

    client_id = forms.CharField(
        label='ID de Cliente',
        required=False,
        # help_text='',
        )

    name = forms.CharField(
        label='Nombre/Razon Social',
        required=False,
        )
    issue = forms.CharField(
        label='Asunto',
        required=False,
        )
    referred_by = forms.CharField(
        label='Referido por',
        required=False,
        )

    phone_number = forms.IntegerField(
        label='Telefono',
        required=False,
        )

    email = forms.EmailField(
        label='Correo electronico',
        required=False,)

    def __init__(self, *args, **kwargs):
        super(IdForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML("<p>Si ya tienes un identificador de cliente, por favor introducelo aqui.</p><br>"),
            'client_id',
            HTML("<hr><p>Si no, por favor provee los siguientes datos, para irnos conociendo.</p><br>"),
            'name',
            'issue',
            'referred_by',
            'phone_number',
            'email',
            FormActions(
                Submit('submit', 'Finalizar'),
            )
        )


class AddAppointmentForm(forms.Form):

    area = forms.ChoiceField(
        label="Que area?",
        choices=((None, "---------"), ('penal', "Penal"), ('mercantil', "Mercantil")),
        required=True
        )

    professional = DynamicChoiceField(
        label="Que profesional?",
        required=True
        )

    dateTime = DynamicChoiceField(
        label="Cuando te viene bien?",
        required=True
        )

    def __init__(self, *args, **kwargs):
        super(AddAppointmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'area',
            'professional',
            'dateTime',
            FormActions(
                Submit('submit', 'Solicitar esta cita'),
            )
        )
