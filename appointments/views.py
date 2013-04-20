#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from appointments.forms import AddAppointmentForm


def add(request):
    """
    """
    if request.method == 'POST':
        print "post"
        form = AddAppointmentForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            print "valid"
            # return HttpResponseRedirect('/thanks/')
        else:
            print form.errors
    else:
        form = AddAppointmentForm()
    # form = AddAppointmentForm()

    return render_to_response('get_appointment.templ',
                              {'appointment_form': form, },
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
        response.write("<option value=\"1\">Sabado 25 - 11:00</option>")
    elif professional == "prof2":
        response.write("<option value=\"2\">Domingo 30 - 16:45</option>")
    elif professional == "prof3":
        response.write("<option value=\"2\">Domingo 22 - 15:45</option>")
    elif professional == "prof4":
        response.write("<option value=\"2\">Lunes 30 - 12:15</option>")
    return response


def get_time_slots_area(request, area, date=None, time=None):
    response = HttpResponse()
    response.write("<option value=\"None\">---------</option>")
    if area == "mercantil":
        response.write("<option value=\"1\">Sabado 25 - 11:00</option>")
        response.write("<option value=\"2\">Domingo 30 - 16:45</option>")
    elif area == "penal":
        response.write("<option value=\"2\">Domingo 22 - 15:45</option>")
        response.write("<option value=\"2\">Lunes 30 - 12:15</option>")
    return response
