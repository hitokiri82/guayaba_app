#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

from schedule.models import Event
from schedule.forms import EventForm

from datetime import datetime, timedelta


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
