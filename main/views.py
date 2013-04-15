#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout


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
