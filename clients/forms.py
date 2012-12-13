#!/usr/bin/python
# -*- coding: utf-8 -*-
from clients.models import NaturalClient, LegalClient, ClientAddress, ClientPhoneNumber

from django.forms import ModelForm, ValidationError
from django.forms.models import BaseInlineFormSet

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
            'activity',
            'id_type',
            'id_number',
            'referred_by',
            Fieldset(
                'Representante Legal',
                'representative_last_name',
                'representative_first_name'
            ),
            Fieldset(
                'Persona de contacto',
                'contact_last_name',
                'contact_first_name',
                'contact_phone_number',
                'contact_email',
            ),
        )
        self.fields['representative_last_name'].label = "Apellido"
        self.fields['representative_first_name'].label = "Nombre"
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


class BaseClientPhoneFormSet(BaseInlineFormSet):
    def clean(self):
        super(BaseClientPhoneFormSet, self).clean()
        """Checks that only one number of the set is preferred."""
        if any(self.errors):
            print "found errors in one form"
            # Don't bother validating the formset unless each form is valid on its own
            return
        found_preferred = False
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            #import pdb; pdb.set_trace()
            if form.cleaned_data:
                is_preferred = form.cleaned_data['is_preferred']
                print str(i) + str(is_preferred)
                if found_preferred and is_preferred:
                    print "Solo un numero puede ser elegido como preferido"
                    raise ValidationError("Solo un numero puede ser elegido como preferido")
                else:
                    if is_preferred:
                        found_preferred = True
