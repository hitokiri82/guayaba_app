#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

from datetime import date, datetime


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


def reports_list(request):
    return render_to_response('report_list.templ',
                              context_instance=RequestContext(request))


def reports_test(request):
    return render_to_response('report_test.templ',
                              context_instance=RequestContext(request))


def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    return date(1900, month_number, 1).strftime("%B")


def this_month(request):
    """
    Show calendar of events this month.
    """
    today = datetime.now()
    return calendar(request, today.year, today.month)


def calendar(request, year, month, series_id=None):
    """
    Show calendar of events for a given month of a given year.
    ``series_id``
    The event series to show. None shows all event series.

    """

    my_year = int(year)
    my_month = int(month)
    # my_calendar_from_month = datetime(my_year, my_month, 1)
    # my_calendar_to_month = datetime(my_year, my_month, monthrange(my_year, my_month)[1])

    # my_events = Event.objects.filter(date_and_time__gte=my_calendar_from_month).filter(date_and_time__lte=my_calendar_to_month)
    # if series_id:
    #     my_events = my_events.filter(series=series_id)

    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    my_previous_year = my_year
    my_previous_month = my_month - 1
    if my_previous_month == 0:
        my_previous_year = my_year - 1
        my_previous_month = 12
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == 13:
        my_next_year = my_year + 1
        my_next_month = 1
    my_year_after_this = my_year + 1
    my_year_before_this = my_year - 1
    return render_to_response("cal_test.templ", {    'events_list': None ,
                                                        'month': my_month,
                                                        'month_name': named_month(my_month),
                                                        'year': my_year,
                                                        'previous_month': my_previous_month,
                                                        'previous_month_name': named_month(my_previous_month),
                                                        'previous_year': my_previous_year,
                                                        'next_month': my_next_month,
                                                        'next_month_name': named_month(my_next_month),
                                                        'next_year': my_next_year,
                                                        'year_before_this': my_year_before_this,
                                                        'year_after_this': my_year_after_this,
    }, context_instance=RequestContext(request))
