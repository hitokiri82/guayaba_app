#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import locale

from main.models import Address, PhoneNumber


NAT_ID_TYPES = (
    (u'PSP', _(u'Pasaporte')),
    (u'NIE', _(u'NIE')),
    (u'DNI', _(u'DNI')),
    (u'OTR', _(u'Otros')),
)

CORP_ID_TYPES = (
    (u'CIF', _(u'CIF')),
)


def t_as_dict(t_list, key):
    for t in t_list:
        if t[0] == key:
            return t[1]
    return None


class Referrer(models.Model):
    """The entity that referred a client"""
    class Meta:
        verbose_name = _('Referente')
        verbose_name_plural = _('Referentes')

    referrer_as_client = models.ForeignKey('Client', blank=True, null=True)
    name = models.CharField(_('Nombre'), max_length=50, blank=True, null=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        """
        If a Referrer is also a Client, then name must be empty
        """
        if self.referrer_as_client is not None:
            if self.name:
                raise ValidationError(_('Si se establece un cliente como referente, el campo Nombre desde permanecer vacio'))
        elif not self.name:
            raise ValidationError(_('Si no se relaciona al referente con un cliente actual, debe indicar un Nombre para el mismo'))

    def __unicode__(self):
        if self.referrer_as_client is not None:
            return unicode(self.referrer_as_client)
        else:
            return self.name


class ClientPhoneNumber(PhoneNumber):
    class Meta:
        verbose_name = _('Telefono de Cliente')
        verbose_name_plural = _('Telefonos de Clientes')

    client = models.ForeignKey('Client', verbose_name=_(u'Cliente'))
    is_preferred = models.BooleanField(_('Preferido'), default=False)

    def __unicode__(self):
        return unicode(self.id)


class Client(models.Model):
    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    created_date = models.DateField(_(u'Fecha Creación'), auto_now_add=True)
    modified_date = models.DateField(_(u'Fecha Modificación'), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_('Creado por'), related_name='created_clients')
    modified_by = models.ForeignKey(User, verbose_name=_('Modificado por'), related_name='modified_cliets')
    referred_by = models.ForeignKey(Referrer, verbose_name=_('Referido por'), blank=True, null=True)

    def is_natural(self):
        try:
            self.naturalclient
            return True
        except:
            return False

    def is_legal(self):
        try:
            self.legalclient
            return True
        except:
            return False

    def get_client_type(self):
        try:
            self.naturalclient
            return 'natural'
        except Client.DoesNotExist:
            try:
                self.legalclient
                return 'legal'
            except Client.DoesNotExist:
                raise Exception('Client not attached to a subclass')

    def get_name(self):
        if self.is_natural():
            return unicode(self.naturalclient)
        else:
            return unicode(self.legalclient)

    def print_as_html(self):
        if self.is_legal():
            return self.legalclient.print_as_html()
        else:
            return self.naturalclient.print_as_html()

    def __cmp__(self, other):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        return locale.strcoll(self.get_name(), other.get_name())

    def __unicode__(self):
        return unicode(self.get_name())


class NaturalClient(Client):
    class Meta:
        verbose_name = _('Cliente Natural')
        verbose_name_plural = _('Clientes Naturales')

    name = models.CharField(_('Nombre'), max_length=25)
    name_2 = models.CharField(_('Segundo Nombre'), max_length=25, blank=True, null=True)
    last_name = models.CharField(_('Apellido'), max_length=25)
    last_name_2 = models.CharField(_('Segundo Apellido'), max_length=25, blank=True, null=True)
    id_type = models.CharField(_('Tipo de ID'), max_length=3, choices=NAT_ID_TYPES, null=True, blank=True)
    id_number = models.CharField(_('Numero de ID'), max_length=15, null=True, blank=True)
    email = models.CharField(_('E-mail'), max_length=50, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.last_name + " " + self.name)

    def clean(self):
        from django.core.exceptions import ValidationError
        """
        If Client has an id_type it must also have an id_number
        """
        if (self.id_type or self.id_number) and not (self.id_type and self.id_number):
            raise ValidationError(_('El tipo y el numero de ID deben estar ambos llenos o ambos vacios'))

    def print_as_html(self):
        output = """ %s %s %s %s <br>
                    <strong>%s:</strong> %s <br>
                    <a href='mailto:%s'>%s</a>
                """ % (self.name,
                       self.name_2,
                       self.last_name,
                       self.last_name_2,
                       t_as_dict(NAT_ID_TYPES, self.id_type),
                       self.id_number,
                       self.email,
                       self.email)
        return output


class LegalClient(Client):
    class Meta:
        verbose_name = _('Cliente Juridico')
        verbose_name_plural = _('Clientes Juridicos')

    corporate_name = models.CharField(_('Razon Social'), max_length=50)
    contact_last_name = models.CharField(_('Apellido de persona de contacto'), max_length=25, blank=True, null=True)
    contact_first_name = models.CharField(_('Nombre de persona de contacto'), max_length=25, blank=True, null=True)
    contact_phone_number = models.CharField(_('Telefono de persona de contacto'), max_length=20, blank=True, null=True)
    contact_email = models.CharField(_('E-mail de persona de contacto'), max_length=50, blank=True, null=True)
    id_type = models.CharField(_('Tipo de ID'), max_length=3, choices=CORP_ID_TYPES, null=True, blank=True)
    id_number = models.CharField(_('Numero de ID'), max_length=15, null=True, blank=True)
    representative_last_name = models.CharField(_('Apellido de representante legal'), max_length=25, blank=True, null=True)
    representative_first_name = models.CharField(_('Nombre de representante legal'), max_length=25, blank=True, null=True)
    activity = models.CharField(_(u'Actividad'), max_length=50, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.corporate_name)

    def clean(self):
        from django.core.exceptions import ValidationError
        """
        If Client has an id_type it must also have an id_number
        """
        if (self.id_type or self.id_number) and not (self.id_type and self.id_number):
            raise ValidationError(_('El tipo y el numero de ID deben estar ambos llenos o ambos vacios'))

    def print_as_html(self):
        output = """ %s <br>
                     %s: %s <br>
                     <strong>Representante Legal:</strong> <br>
                     %s %s <br>
                     <strong>Persona Contacto:</strong> <br>
                     %s %s <br>
                     <strong>Telefono:</strong> %s <br>
                     <a href='mailto:%s'>%s</a>
                """ % (self.corporate_name,
                       t_as_dict(CORP_ID_TYPES, self.id_type),
                       self.id_number,
                       self.representative_first_name,
                       self.representative_last_name,
                       self.contact_first_name,
                       self.contact_last_name,
                       self.contact_phone_number,
                       self.contact_email,
                       self.contact_email)
        return output


class ClientAddress(Address):

    class Meta:
        verbose_name = _('Direccion')
        verbose_name_plural = _('Direcciones')

    client = models.OneToOneField(Client, verbose_name=(_(u'Cliente')), primary_key=True)
