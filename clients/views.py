#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

from clients.models import Client
from clients.forms import NaturalClientForm, LegalClientForm


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
