#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


NAT_ID_TYPES = (
    (u'PSP', _(u'Pasaporte')),
    (u'NIE', _(u'NIE')),
    (u'CIF', _(u'CIF')),
)

CORP_ID_TYPES = (
    (u'CIF', _(u'CIF')),
)


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

    def get_name(self):
        try:
            name = self.naturalclient.last_name + ", " + self.naturalclient.name
        except Client.DoesNotExist:
            try:
                name = self.legalclient.corporate_name
            except Client.DoesNotExist:
                raise Exception('Client not attached to a subclass')
        return name

    def __unicode__(self):
        return unicode(self.id)


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

    client = models.ForeignKey(Client)
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
        return unicode(self.id)


class Event(models.Model):
    class Meta:
        verbose_name = _('Evento')
        verbose_name_plural = _('Eventos')

    owner = models.ForeignKey(User)
    case = models.ForeignKey(Case)
    date = models.DateField(_('Fecha'), blank=True, null=True)
    begin_time = models.TimeField(_('Hora de Inicio'), blank=True, null=True)
    end_time = models.TimeField(_('Hora Fin'), blank=True, null=True)
    description = models.CharField(_('Descripcion'), max_length=50)
    comments = models.TextField(_('Comentarios'), blank=True, null=True)
    status = models.CharField(_('Estado/Status'), max_length=2, blank=True, null=True)
    result = models.CharField(_('Resultado'), max_length=2, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.id)


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

    owner = models.ForeignKey(User)
    is_main = models.BooleanField(_('Principal'))
    preferred_color = models.CharField(_('Color Preferido'), max_length=5, default='blue')

    def __unicode__(self):
        return unicode(self.owner.username + " " + unicode(self.id))


# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     firm = models.ForeignKey(Firm)
#     ownSchedule = models.OneToOneField(Schedule, related_name='owner')
#     viewsSchedule = models.ManyToManyField(Schedule, related_name='users_with_view_access', blank=True, null=True)
