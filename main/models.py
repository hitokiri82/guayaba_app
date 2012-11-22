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

STATUSES = (
    (u'O', _(u'Abierto')),
    (u'D', _(u'Realizado')),
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


class Address(models.Model):
    class Meta:
        verbose_name = _('Dirección')
        verbose_name_plural = _('Direcciones')

    street_1 = models.CharField(_('Calle/Portal/Piso'), max_length=20, blank=True, null=True)
    street_2 = models.CharField(_('Calle/Portal/Piso (Cont)'), max_length=20, blank=True, null=True)
    municipality = models.CharField(_('Ciudad'), max_length=20, blank=True, null=True)
    administrative_area = models.CharField(_('Ciudad'), max_length=20, blank=True, null=True)
    subadministrative_area = models.CharField(_('Ciudad'), max_length=20, blank=True, null=True)
    postal_code = models.CharField(_('Ciudad'), max_length=20, blank=True, null=True)
    country = models.CharField(_('Ciudad'), max_length=20, blank=True, null=True)

    def __unicode__(self):
        pass


class Client(models.Model):
    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    # client_type = models.CharField(_('Tipo de Cliente'), max_length=1)
    phone_1 = models.CharField(_('Telefono 1'), max_length=20, blank=True, null=True)
    phone_2 = models.CharField(_('Telefono 2'), max_length=20, blank=True, null=True)
    phone_3 = models.CharField(_('Telefono 3'), max_length=20, blank=True, null=True)
    street = models.CharField(_('Calle/Av.'), max_length=20, blank=True, null=True)
    postal_zone = models.CharField(_('Zona Postal'), max_length=20, blank=True, null=True)
    country = models.CharField(_('Pais'), max_length=20, blank=True, null=True)
    city = models.CharField(_('Ciudad'), max_length=20, blank=True, null=True)
    state = models.CharField(_('Estado/Provincia'), max_length=20, blank=True, null=True)
    created_date = models.DateField(_('Fecha Creación'), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_('Creado por'))
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


class Case(models.Model):
    class Meta:
        verbose_name = _('Caso')
        verbose_name_plural = _('Casos')

    client = models.ForeignKey(Client, verbose_name=_('Cliente'))
    created_date = models.DateField(_('Fecha de Creación'), auto_now_add=True)
    begin_date = models.DateField(_('Fecha Inicio'), blank=True, null=True)
    end_date = models.DateField(_('Fecha Fin'), blank=True, null=True)
    description = models.CharField(_('Descripcion'), max_length=50)
    status = models.CharField(_('Estado/Status'), max_length=2, blank=True, null=True)
    result = models.CharField(_('Resultado'), max_length=2, blank=True, null=True)
    comments = models.TextField(_('Comentarios'), blank=True, null=True)
    budget = models.DecimalField(_('Presupuesto'), max_digits=10, decimal_places=2)
    collected = models.DecimalField(_('Monto Cobrado'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('Moneda'), max_length=3, blank=True, null=True)

    def __unicode__(self):
        return unicode(unicode(self.client) + " - " + unicode(self.description))


class Event(models.Model):
    class Meta:
        verbose_name = _('Evento')
        verbose_name_plural = _('Eventos')

    owner = models.ForeignKey(User, verbose_name=_('Usuario'))
    client = models.ForeignKey(Client, verbose_name=_('Cliente'), blank=True, null=True)
    case = models.ForeignKey(Case, verbose_name=_('Caso'), blank=True, null=True)
    date = models.DateField(_('Fecha'))
    begin_time = models.TimeField(_('Hora de Inicio'))
    duration = models.IntegerField(_(u'Duración'), blank=True, null=True)
    description = models.CharField(_(u'Descripción'), max_length=50)
    comments = models.TextField(_('Comentarios'), blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUSES, blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        """
        If an Event has a case assigned, it must also have a client assigned and the client-case
        relation must be consistent.
        """
        if self.case is not None:
            if self.client is None:
                self.client = self.case.client
            else:
                if self.case.client != self.client:
                    raise ValidationError(_('El cliente del evento no coincide con el cliente del caso asignado'))

    def __unicode__(self):
        return unicode(str(self.owner) + u" " + str(self.date))


class Firm(models.Model):
    class Meta:
        verbose_name = _('Despacho')
        verbose_name_plural = _('Despachos')

    name = models.CharField(_('Nombre'), max_length=50)

    def __unicode__(self):
        return self.name


class Schedule(models.Model):
    class Meta:
        verbose_name = _('Agenda')
        verbose_name_plural = _('Agendas')

    owner = models.ForeignKey(User, verbose_name=_('Usuario'))
    is_main = models.BooleanField(_('Principal'))
    preferred_color = models.CharField(_('Color Preferido'), max_length=5, default='blue')

    def __unicode__(self):
        return unicode(self.owner.username + " " + unicode(self.id))


# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     firm = models.ForeignKey(Firm)
#     ownSchedule = models.OneToOneField(Schedule, related_name='owner')
#     viewsSchedule = models.ManyToManyField(Schedule, related_name='users_with_view_access', blank=True, null=True)
