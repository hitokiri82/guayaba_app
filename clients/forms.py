#!/usr/bin/python
# -*- coding: utf-8 -*-
from clients.models import NaturalClient, LegalClient, ClientAddress, ClientPhoneNumber

from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class NaturalClientForm(ModelForm):
    class Meta:
        model = NaturalClient
        exclude = ('date_created', 'created_by', 'modified_by', 'address',)

    def __init__(self, *args, **kwargs):
        super(NaturalClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'name',
            'name_2',
            'last_name',
            'last_name_2',
            'id_type',
            'id_number',
            'email',
            'referred_by'
        )


class LegalClientForm(ModelForm):
    class Meta:
        model = LegalClient
        exclude = ('date_created', 'created_by', 'modified_by', 'address', )

    def __init__(self, *args, **kwargs):
        super(LegalClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'corporate_name',
            'id_type',
            'id_number',
            Fieldset(
                'Responsable Juridico',
                'responsible_last_name',
                'responsible_first_name'
            ),
            Fieldset(
                'Persona de contacto',
                'contact_last_name',
                'contact_first_name',
                'contact_phone_number',
                'contact_email',
            ),
            'referred_by',
        )
        self.fields['responsible_last_name'].label = "Apellido"
        self.fields['responsible_first_name'].label = "Nombre"
        self.fields['contact_last_name'].label = "Apellido"
        self.fields['contact_first_name'].label = "Nombre"
        self.fields['contact_phone_number'].label = "Numero de Telefono"
        self.fields['contact_email'].label = "E-mail"


class AddressForm(ModelForm):
    class Meta:
        model = ClientAddress
        exclude = ('date_created', 'created_by', 'modified_by', 'client')

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'street_1',
            'street_2',
            'municipality',
            'subadministrative_area',
            'administrative_area',
            'postal_code',
            'country',
        )


class ClientPhoneNumberForm(ModelForm):
    class Meta:
        model = ClientPhoneNumber
        exclude = ('client', )

    def __init__(self, *args, **kwargs):
        super(ClientPhoneNumberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'kind',
            'number',
            'is_preferred',
        )
