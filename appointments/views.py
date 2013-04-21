#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from appointments.forms import AddAppointmentForm, IdForm
from appointments.models import TimeSlot

from schedule.models import Event
# def mockup(request):
#     form = AddAppointmentForm()

#     return render_to_response('mockup.templ',
#                                {'appointment_form': form, },
#                                context_instance=RequestContext(request))


def external_add1(request):
    """
    """
    if request.method == 'POST':
        print "post"
        form = AddAppointmentForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            request.session['form1'] = form.cleaned_data
            return HttpResponseRedirect(reverse('appointments.views.external_add2'))
        else:
            print form.errors
    else:
        form = AddAppointmentForm()

    return render_to_response('mockup1.templ',
    # return render_to_response('get_appointment1.templ',
                              {'appointment_form': form, },
                               context_instance=RequestContext(request))


def external_add2(request):
    """
    """
    if request.method == 'POST':
        form = IdForm(request.POST)
        if form.is_valid():
            cd = request.session.get('form1')
            ts = TimeSlot.objects.get(pk=cd['dateTime'])
            u = User.objects.get(username='prueba')
            e = Event(owner=u,
                      date=ts.date,
                      begin_time=ts.begin_time,
                      description='WEB: ' + form.cleaned_data['name'])
            e.save()
            return HttpResponseRedirect(reverse('appointments.views.external_add3'))
        else:
            print form.errors
    else:
        form = IdForm()

    return render_to_response('mockup2.templ',
    # return render_to_response('get_appointment2.templ',
                              {'id_form': form, },
                               context_instance=RequestContext(request))


def external_add3(request):
    """
    """
    return render_to_response('mockup3.templ',
                               context_instance=RequestContext(request))


def get_professionals(request, area):
    response = HttpResponse()
    response.write("<option value=\"None\">---------</option>")
    response.write("<option value=\"All\">Me da igual</option>")
    if area == 'mercantil':
        response.write("<option value=\"prof1\">El uno</option>")
        response.write("<option value=\"prof2\">El otro</option>")
    elif area == 'penal':
        response.write("<option value=\"prof3\">El mejor</option>")
        response.write("<option value=\"prof4\">El peor</option>")
    return response


def get_time_slots(request, professional, date=None, time=None):
    response = HttpResponse()
    response.write("<option value=\"None\">---------</option>")
    if professional == "prof1":
        response.write("<option value=\"1\">Domingo 21 - 14:00</option>")
    elif professional == "prof2":
        response.write("<option value=\"2\">Lunes 22 - 16:00</option>")
    elif professional == "prof3":
        response.write("<option value=\"3\">Domingo 21 - 17:45</option>")
    elif professional == "prof4":
        response.write("<option value=\"4\">Lunes 22 - 11:15</option>")
    return response


def get_time_slots_area(request, area, date=None, time=None):
    response = HttpResponse()
    response.write("<option value=\"None\">---------</option>")
    if area == "mercantil":
        response.write("<option value=\"1\">Domingo 21 - 14:00</option>")
        response.write("<option value=\"2\">Lunes 22 - 16:00</option>")
    elif area == "penal":
        response.write("<option value=\"2\">Domingo 21 - 17:45</option>")
        response.write("<option value=\"2\">Lunes 22 - 11:15</option>")
    return response
