#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory

from clients.models import Client, NaturalClient, LegalClient, ClientPhoneNumber, ClientAddress
from clients.forms import NaturalClientForm, LegalClientForm, AddressForm, ClientPhoneNumberForm


class Breadcrumb():
    """docstring for Breadcrumb"""
    def __init__(self):
        self.items = []

    def print_as_html(self):
        if self.items:
            output = "<ul class=\"breadcrumb\">\n"
            for item in self.items[:-1]:
                output += "<li><a href=\"%s\">%s</a><span class=\"divider\">/</span></li>\n" % (item[0], item[1])
            output += "<li class=\"active\">%s</li>\n" % self.items[-1][1]
            output += "</ul>\n"
        return output


def clients(request):
    """
    """
    b = Breadcrumb()
    b.items.append((request.path, 'Clientes'))
    request.session['breadcrumb'] = b

    if request.method == 'POST':
        print "POST data detected "
        if 'confirm_remove' in request.POST:
            print "Remove request detected"
            client_id = request.POST['client_id']
            client = Client.objects.get(pk=client_id)
            client.delete()
    clients = list(Client.objects.all())
    clients.sort()

    return render_to_response('clients.templ',
                              {'clients': clients, },
                               context_instance=RequestContext(request))


def client(request, client_id):
    """
        This view has to get the data related to the client as well as all the
        cases that are related with this client.
        I must also handle edition of the client.
    """
    client = get_object_or_404(Client, pk=client_id)
    b = request.session['breadcrumb']
    b.items = [b.items[0], ((request.path, client.get_name()))]
    request.session['breadcrumb'] = b

    return render_to_response('client.templ',
                              {'client': client},
                               context_instance=RequestContext(request))


def client_basic(request, client_type, client_id=None):
    """
    """
    if client_type == "natural":
        form_class = NaturalClientForm
        client_class = NaturalClient
    elif client_type == "legal":
        form_class = LegalClientForm
        client_class = LegalClient
    else:
        raise Exception("Error en el URL")

    b = request.session['breadcrumb']
    if client_id is not None:
        instance = get_object_or_404(client_class, pk=client_id)
        b.items.append((request.path, 'Editar datos basicos'))
    else:
        b.items.append((request.path, 'Crear datos basicos'))
        instance = client_class()

    if request.method == 'POST':
        client_form = form_class(request.POST, instance=instance)

        if client_form.is_valid():
            print "Client is valid"
            new_client = client_form.save(commit=False)
            new_client.created_by = request.user
            new_client.modified_by = request.user
            new_client.save()
            print "Client saved"
            return HttpResponseRedirect(reverse('clients.views.client', kwargs={'client_id': new_client.id}) + "#profile")
        else:
            print "Its not valid"
    else:
        client_form = form_class(instance=instance)

    return render_to_response('client_basic.templ',
                              {'client_form': client_form},
                               context_instance=RequestContext(request))


def create_address(request, client_id):
    """
    """
    client = get_object_or_404(Client, pk=client_id)

    b = request.session['breadcrumb']
    try:
        instance = client.clientaddress
        b.items.append((request.path, 'Editar direccion'))
    except ClientAddress.DoesNotExist:
        instance = ClientAddress()
        b.items.append((request.path, 'Crear direccion'))

    if request.method == 'POST':
        address_form = AddressForm(request.POST, instance=instance)
        if address_form.is_valid():
            address_form.save()
            client.clientaddress = instance
            client.save()
            return HttpResponseRedirect(reverse('clients.views.client', kwargs={'client_id': client.id}))
    else:
        address_form = AddressForm(instance=instance)

    return render_to_response('create_address.templ',
                              {'address_form': address_form},
                               context_instance=RequestContext(request))


def phones(request, client_id):
    PhonesFormSet = inlineformset_factory(Client, ClientPhoneNumber, extra=1)
    client = Client.objects.get(pk=client_id)
    formset = PhonesFormSet(instance=client)
    if request.method == "POST":
        formset = PhonesFormSet(request.POST, instance=client)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('clients.views.phones', kwargs={'client_id': client.id}))
    else:
        formset = PhonesFormSet(instance=client)
    return render_to_response('phones.templ',
                              {'formset': formset,
                               'client_id': client_id, },
                               context_instance=RequestContext(request))
