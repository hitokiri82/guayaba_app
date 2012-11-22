#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


STATUSES = (
    (u'O', _(u'Abierto')),
    (u'D', _(u'Realizado')),
)


class Case(models.Model):
    class Meta:
        verbose_name = _('Caso')
        verbose_name_plural = _('Casos')

    client = models.ForeignKey('clients.Client', verbose_name=_('Cliente'))
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
    client = models.ForeignKey('clients.Client', verbose_name=_('Cliente'), blank=True, null=True)
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
