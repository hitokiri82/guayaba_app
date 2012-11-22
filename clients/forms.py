#!/usr/bin/python
# -*- coding: utf-8 -*-
from clients.models import NaturalClient, LegalClient

from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class NaturalClientForm(ModelForm):
    class Meta:
        model = NaturalClient
        exclude = ('date_created', 'created_by', )

    def __init__(self, *args, **kwargs):
        super(NaturalClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'natClientForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            'name',
            'name_2',
            'last_name',
            'last_name_2',
            'id_type',
            'id_number',
            'email',
            'phone_1',
            'phone_2',
            'phone_3',
            'street',
            'city',
            'state',
            'postal_zone',
            'country',
            'referred_by',
            FormActions(
                Submit('add_nat_client', u'Añadir'),
                Button('cancel', u'Cancelar'),
            )
        )


class LegalClientForm(ModelForm):
    class Meta:
        model = LegalClient
        exclude = ('date_created', 'created_by', )

    def __init__(self, *args, **kwargs):
        super(LegalClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'natClientForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            'corporate_name',
            'id_type',
            'id_number',
            'contact_last_name',
            'contact_first_name',
            'contact_phone_number',
            'contact_email',
            'phone_1',
            'phone_2',
            'phone_3',
            'street',
            'city',
            'state',
            'postal_zone',
            'country',
            'referred_by',
            FormActions(
                Submit('add_legal_client', u'Añadir'),
                Button('cancel', u'Cancelar'),
            )
        )
