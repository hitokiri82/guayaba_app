#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


NUM_TYPES = (
    (u'O', _(u'Oficina')),
    (u'H', _(u'Casa')),
    (u'M', _(u'Móvil')),
)


class PhoneNumber(models.Model):
    class Meta:
        verbose_name = _('Telefono')
        verbose_name_plural = _('Telefonos')

    kind = models.CharField(_('Tipo de Numero'), max_length=1, choices=NUM_TYPES, default='O')
    number = models.CharField(_('Numero'), max_length=20)

    def __unicode__(self):
        return unicode(self.id)


class Address(models.Model):
    class Meta:
        verbose_name = _('Direccion')
        verbose_name_plural = _('Direcciones')

    street_1 = models.CharField(_('Calle/Portal/Piso'), max_length=50)
    street_2 = models.CharField(_('Calle/Portal/Piso (Cont)'), max_length=50, blank=True, null=True)
    municipality = models.CharField(_('Ciudad'), max_length=30)
    subadministrative_area = models.CharField(_('Provincia'), max_length=20, blank=True, null=True)
    administrative_area = models.CharField(_('Comunidad Autonoma'), max_length=20, blank=True, null=True)
    postal_code = models.CharField(_('Zona Postal'), max_length=20, blank=True, null=True)
    country = models.CharField(_('Pais'), max_length=20)

    def __unicode__(self):
        return unicode(self.id)

    def print_as_html(self):
        output = """ %s <br>
                     %s <br>
                     %s %s <br>
                     %s <br>
                     %s <br>
                     %s <br>
                """ % (self.street_1,
                       self.street_2,
                       self.municipality,
                       self.postal_code,
                       self.subadministrative_area,
                       self.administrative_area,
                       self.country)
        return output


class Firm(models.Model):
    class Meta:
        verbose_name = _('Despacho')
        verbose_name_plural = _('Despachos')

    name = models.CharField(_('Nombre'), max_length=50)

    def __unicode__(self):
        return self.name
