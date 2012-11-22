#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import locale


NAT_ID_TYPES = (
    (u'PSP', _(u'Pasaporte')),
    (u'NIE', _(u'NIE')),
    (u'DNI', _(u'DNI')),
    (u'OTR', _(u'Otros')),
)

CORP_ID_TYPES = (
    (u'CIF', _(u'CIF')),
)

NUM_TYPES = (
    (u'P', _(u'Profesional')),
    (u'H', _(u'Casa')),
    (u'M', _(u'Mobil')),
)


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


class PhoneNumber(models.Model):
    class Meta:
        verbose_name = _('Telefono')
        verbose_name_plural = _('Telefonos')

    kind = models.CharField(_('Tipo de Numero'), max_length=1, choices=NUM_TYPES, default='P')
    number = models.CharField(_('Numero'), max_length=20, blank=True, null=True)
    is_preferred = models.BooleanField(_('Preferido'), default=False)

    def __unicode__(self):
        pass


class ClientPhoneNumber(PhoneNumber):

    client = models.ForeignKey('Client', verbose_name=_(u'Cliente'))

    def __unicode__(self):
        pass


class Address(models.Model):
    class Meta:
        verbose_name = _('Direccion')
        verbose_name_plural = _('Direcciones')

    street_1 = models.CharField(_('Calle/Portal/Piso'), max_length=20, blank=True, null=True)
    street_2 = models.CharField(_('Calle/Portal/Piso (Cont)'), max_length=20, blank=True, null=True)
    municipality = models.CharField(_('Ciudad'), max_length=20, blank=True, null=True)
    administrative_area = models.CharField(_('Comunidad Autonoma'), max_length=20, blank=True, null=True)
    subadministrative_area = models.CharField(_('Provincia'), max_length=20, blank=True, null=True)
    postal_code = models.CharField(_('Zona Postal'), max_length=20, blank=True, null=True)
    country = models.CharField(_('Pais'), max_length=20, blank=True, null=True)

    def __unicode__(self):
        pass


class Client(models.Model):
    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    address = models.ForeignKey(Address, verbose_name=(_('Direccion')))
    created_date = models.DateField(_('Fecha Creacion'), auto_now_add=True)
    modified_date = models.DateField(_('Fecha Modificación'), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_('Creado por'), related_name='created_users')
    modified_by = models.ForeignKey(User, verbose_name=_('Modificado por'), related_name='modified_users')
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
            return 'N'
        except Client.DoesNotExist:
            try:
                self.legalclient
                return 'L'
            except Client.DoesNotExist:
                raise Exception('Client not attached to a subclass')

    def get_name(self):
        if self.get_client_type() == 'N':
            # name = self.naturalclient.last_name + ", " + self.naturalclient.name
            return unicode(self.naturalclient)
        else:
            return unicode(self.legalclient)

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
    id_type = models.CharField(_('Tipo de ID'), max_length=3, choices=NAT_ID_TYPES)
    id_number = models.CharField(_('Numero de ID'), max_length=15)
    email = models.CharField(_('E-mail'), max_length=50, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.last_name + " " + self.name)


class LegalClient(Client):
    class Meta:
        verbose_name = _('Cliente Juridico')
        verbose_name_plural = _('Clientes Juridicos')

    corporate_name = models.CharField(_('Razon Social'), max_length=50)
    contact_last_name = models.CharField(_('Apellido de persona de contacto'), max_length=25, blank=True, null=True)
    contact_first_name = models.CharField(_('Nombre de persona de contacto'), max_length=25, blank=True, null=True)
    contact_phone_number = models.CharField(_('Telefono de persona de contacto'), max_length=20, blank=True, null=True)
    contact_email = models.CharField(_('E-mail de persona de contacto'), max_length=50, blank=True, null=True)
    id_type = models.CharField(_('Tipo de ID'), max_length=3, choices=CORP_ID_TYPES)
    id_number = models.CharField(_('Numero de ID'), max_length=15)

    def __unicode__(self):
        return unicode(self.corporate_name)
