#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import logging

logger = logging.getLogger(__name__)

LEGAL_AREAS = (
    (u'M', _(u'Mercantil')),
    (u'P', _(u'Penal')),
    (u'E', _(u'Extranjeria')),
)

ACTION_TYPES = (
    (u'P', _(u'Providencia')),
    (u'A', _(u'Auto')),
    (u'S', _(u'Sentencia')),
    (u'D', _(u'Dilegencia')),
)

# class modelllll(models.Model):
#     """The entity that referred a client"""
#     class Meta:
#         verbose_name = _('Referente')
#         verbose_name_plural = _('Referentes')

#     referrer_as_client = models.ForeignKey('Client', blank=True, null=True)
#     name = models.CharField(_('Nombre'), max_length=50, blank=True, null=True)

#     def clean(self):
#         from django.core.exceptions import ValidationError
#         """
#         If a Referrer is also a Client, then name must be empty
#         """
#         if self.referrer_as_client is not None:
#             if self.name:
#                 raise ValidationError(_('Si se establece un cliente como referente, el campo Nombre desde permanecer vacio'))
#         elif not self.name:
#             raise ValidationError(_('Si no se relaciona al referente con un cliente actual, debe indicar un Nombre para el mismo'))

#     def __unicode__(self):
#         if self.referrer_as_client is not None:
#             return unicode(self.referrer_as_client)
#         else:
#             return self.name


class Court(models.Model):
    class Meta:
        verbose_name = _(u'Juzgado')
        verbose_name_plural = _(u'Juzgados')

    name = models.CharField(_(u'Nombre'), max_length=50)

    def __unicode__(self):
        return unicode(self.name)


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
    # budget = models.DecimalField(_('Presupuesto'), max_digits=10, decimal_places=2)
    # collected = models.DecimalField(_('Monto Cobrado'), max_digits=10, decimal_places=2)
    # currency = models.CharField(_('Moneda'), max_length=3, blank=True, null=True)

    def __unicode__(self):
        return unicode(unicode(self.client) + " - " + unicode(self.description))


class Procedure(models.Model):
    class Meta:
        verbose_name = _(u'Procedimiento')
        verbose_name_plural = _(u'Procedimientos')

    def __unicode__(self):
        return unicode(self.id)

    description = models.CharField(_(u'Description'), max_length=50)
    area = models.CharField(_(u'Area'), max_length=1, choices=LEGAL_AREAS)
    court = models.ForeignKey(Court, verbose_name=Court._meta.verbose_name)
    derived_from = models.ForeignKey('Procedure', verbose_name=_(u'Hijo de'), null=True, blank=True)


class Action(models.Model):
    class Meta:
        verbose_name = _(u'Actuación')
        verbose_name_plural = _(u'Actuaciones')

    procedure = models.ForeignKey(Procedure, verbose_name=_(u'Procedimiento'))
    description = models.CharField(_(u'Descripción'), max_length=50)
    notification_date = models.DateField(_(u'Fecha Creación'))
    effect_date = models.DateField(_(u'Fecha Efectiva'))
    act_type = models.CharField(_(u'Tipo'), max_length=1, choices=ACTION_TYPES)

    def __unicode__(self):
        return unicode(self.description)

    def clean(self):
        print self.act_type == 'S'
        print isinstance(self, Sentence)
        if (self.act_type == 'S' or isinstance(self, Sentence)) and not (self.act_type == 'S' and isinstance(self, Sentence)):
            from django.core.exceptions import ValidationError
            e = ValidationError(_(u'Solo las sentencias pueden tener tipo sentencia'))
            logger.error(e)
            raise e


class Sentence(Action):
    class Meta:
        verbose_name = _(u'Sentencia')
        verbose_name_plural = _(u'Sentencias')

    def __init__(self, *args, **kwargs):
        super(Sentence, self).__init__(*args, **kwargs)
        self.act_type = 'S'

    result = models.CharField(_(u'Resultado'), max_length=50)
    costs = models.BooleanField(_(u'Costas'))
    positive = models.BooleanField(_(u'Resultado Positivo'))
