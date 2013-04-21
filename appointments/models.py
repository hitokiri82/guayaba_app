#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeSlot(models.Model):
    class Meta:
        verbose_name = _(u'TimeSlot')
        verbose_name_plural = _(u'TimeSlots')

    def __unicode__(self):
        return unicode(self.id)

    date = models.DateField(_('Fecha'))
    begin_time = models.TimeField(_('Hora de Inicio'))
    duration = models.IntegerField(_(u'Duración'))
