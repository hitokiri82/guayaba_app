#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login

from main.models import Event
from main.forms import EventForm

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
                return HttpResponseRedirect('/schedule/today')
            else:
                # Return a 'disabled account' error message
                error_message = "Su cuenta ha sido desactivada"
        else:
            error_message = "Esa combinacion de usuario y contraseña no existe en el sistema"

    return render_to_response('login.templ', {'error_message': error_message, }, context_instance=RequestContext(request))


def today(request):
    """
        This view has to get all the events from today onwards for the current user, up to a point (for now its a week), it then must generate two event lists: today, and upcoming and send those lists back to the today template.
    """
    user = request.user
    print "Getting events for user" + user.username
    if request.method == 'POST':
        print "POST data detected "
        if 'confirm_remove' in request.POST:
            print "Remove request detected"
            event_id = request.POST['event_id']
            event = Event.objects.get(pk=event_id)
            event.delete()
        if 'add_event' in request.POST:
            print "Add request detected"
            pass

    event_form = EventForm()

    today = datetime.now().date()
    today_plus_7 = today + timedelta(days=7)

    events = Event.objects.filter(owner=user.pk, date__gte=today, date__lte=today_plus_7).order_by('date', 'begin_time')

    print "Total number of events: " + str(events.count())

    todays_events = events.filter(date=today)
    incoming_events = events.exclude(date=today)
    return render_to_response('today.templ', {'todays_events': todays_events, 'incoming_events': incoming_events, 'event_form': event_form}, context_instance=RequestContext(request))

# def index(request):
#     # print request.META['HTTP_ACCEPT_LANGUAGE']
#     if request.method == 'POST':  # If the form has been submitted...
#         form = VisitForm(request.POST)  # A form bound to the POST data
#         if form.is_valid():  # All validation rules pass
#             if form.has_changed():
#                 visit = form.save(commit=False)
#                 ip_address = request.META['REMOTE_ADDR']
#                 if 'referer' in request.session:
#                     referer = request.session['referer']
#                 else:
#                     referer = None
#                 response = loads(urlopen('http://api.hostip.info/get_json.php?ip=' + ip_address).read())
#                 country = response['country_name']
#                 city = response['city']
#                 visit.referer = referer
#                 visit.country = country
#                 visit.city = city
#                 visit.save()
#             return HttpResponseRedirect('/thanks/')  # Redirect after POST
#         else:
#             print form.errors
#     else:
#         form = VisitForm()  # An unbound form
#         if 'HTTP_REFERER' in request.META:
#             request.session['referer'] = request.META['HTTP_REFERER']
#     return render_to_response('poll.html', {'form': form, }, context_instance=RequestContext(request))
