#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

from main.models import Event, Client
from main.forms import EventForm, NaturalClientForm, LegalClientForm

from datetime import datetime, timedelta


def login_view(request):
    error_message = None
    if request.method == 'POST':  # If the form has been submitted...
        input_user = request.POST['user']
        input_password = request.POST['password']
        user = authenticate(username=input_user, password=input_password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/today/')
            else:
                # Return a 'disabled account' error message
                error_message = "Su cuenta ha sido desactivada"
        else:
            error_message = "Esa combinacion de usuario y contraseña no existe en el sistema"

    return render_to_response('login.templ',
                              {'error_message': error_message, },
                              context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def today(request):
    """
        This view has to get all the events from today onwards for the current
        user, up to a point (for now its a week), it then must generate two
        event lists: today, and upcoming and send those lists back to the today
        template.
    """
    user = request.user
    print "User is authenticated: " + str(user.is_authenticated())
    print "Getting events for user " + user.username

    if request.method == 'POST':
        print "POST data detected "
        if 'confirm_remove' in request.POST:
            print "Remove request detected"
            event_id = request.POST['event_id']
            event = Event.objects.get(pk=event_id)
            event.delete()
        if 'add_event' in request.POST:
            print "Add request detected"
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                print "Its valid"
                new_event = event_form.save(commit=False)
                new_event.owner = request.user
                new_event.save()
                del event_form
                print "Saved"
            else:
                print "Its not valid"

    try:
        event_form
    except:
        event_form = EventForm()

    today = datetime.now().date()
    today_plus_7 = today + timedelta(days=7)

    events = Event.objects.filter(owner=user.pk, date__gte=today, date__lte=today_plus_7).order_by('date', 'begin_time')

    print "Total number of events: " + str(events.count())

    todays_events = events.filter(date=today)
    incoming_events = events.exclude(date=today)
    return render_to_response('today.templ',
                              {'todays_events': todays_events,
                               'incoming_events': incoming_events,
                               'event_form': event_form},
                              context_instance=RequestContext(request))


def clients(request):
    """
        This view has to get all the events from today onwards for the
        current user, up to a point (for now its a week), it then must generate
        two event lists: today, and upcoming and send those lists back to the
        today template.
    """

    if request.method == 'POST':
        print "POST data detected "
        if 'confirm_remove' in request.POST:
            print "Remove request detected"
            client_id = request.POST['client_id']
            client = Client.objects.get(pk=client_id)
            client.delete()
        if 'add_nat_client' in request.POST:
            print "Add request detected"
            nat_client_form = NaturalClientForm(request.POST)
            if nat_client_form.is_valid():
                print "Its valid"
                new_nat_client = nat_client_form.save(commit=False)
                new_nat_client.created_by = request.user
                new_nat_client.save()
                del nat_client_form
                print "Saved"
            else:
                print "Its not valid"
        if 'add_legal_client' in request.POST:
            print "Add request detected"
            legal_client_form = LegalClientForm(request.POST)
            if legal_client_form.is_valid():
                print "Its valid"
                new_legal_client = legal_client_form.save(commit=False)
                new_legal_client.created_by = request.user
                new_legal_client.save()
                del legal_client_form
                print "Saved"
            else:
                print "Its not valid"

    try:
        nat_client_form
    except:
        nat_client_form = NaturalClientForm()

    try:
        legal_client_form
    except:
        legal_client_form = LegalClientForm()

    clients = list(Client.objects.all())
    clients.sort()

    return render_to_response('clients.templ',
                              {'clients': clients,
                               'nat_client_form': nat_client_form,
                               'legal_client_form': legal_client_form},
                               context_instance=RequestContext(request))


def client(request, client_id):
    """
        This view has to get the data related to the client as well as all the
        cases that are related with this client.
        I must also handle edition of the client.
    """

    client = Client.objects.get(pk=client_id)
    return render_to_response('client.templ',
                              {'client': client},
                               context_instance=RequestContext(request))
