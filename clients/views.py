#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from clients.models import Client, NaturalClient, LegalClient, ClientPhoneNumber, Address
from clients.forms import NaturalClientForm, LegalClientForm, AddressForm, ClientPhoneNumberForm


class Breadcrumb():
    """docstring for Breadcrumb"""
    def __init__(self):
        self.items = []

    def print_as_html(self):
        # import pdb; pdb.set_trace()
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
    client = Client.objects.get(pk=client_id)
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
        instance = client_class.objects.get(pk=client_id)
        b.items.append((request.path, 'Editar datos basicos'))
    else:
        b.items.append((request.path, 'Crear datos basicos'))
        instance = client_class()

    print b.items

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

    client = Client.objects.get(pk=client_id)

    b = request.session['breadcrumb']
    if client.address:
        instance = client.address
        b.items.append((request.path, 'Editar direccion'))
    else:
        instance = Address()
        b.items.append((request.path, 'Crear direccion'))

    if request.method == 'POST':
        address_form = AddressForm(request.POST, instance=instance)
        if address_form.is_valid():
            address_form.save()
            client.address = instance
            client.save()
            return HttpResponseRedirect(reverse('clients.views.client', kwargs={'client_id': client.id}))
    else:
        address_form = AddressForm(instance=instance)

    return render_to_response('create_address.templ',
                              {'address_form': address_form},
                               context_instance=RequestContext(request))


# def phone_numbers(request, client_id, operation = None, phone_id = None):
def phone_numbers(request, client_id):
    """
    """
    client = Client.objects.get(pk=client_id)
    b = request.session['breadcrumb']
    b.items.append((request.path, 'Telefonos'))

    edit_phone_id = None
    if request.method == 'POST':
        print "POST data detected "
        if 'confirm_remove' in request.POST:
            user_phone_id = request.POST['user_phone_id']
            phone_del = ClientPhoneNumber.objects.get(pk=user_phone_id)
            phone_del.delete()
        if 'confirm_add' in request.POST:
            new_phone_form = ClientPhoneNumberForm(request.POST)
            if new_phone_form.is_valid() and new_phone_form.has_changed():
                new_phone = new_phone_form.save(commit=False)
                new_phone.client = client
                new_phone.save()
                del new_phone_form
        if 'confirm_edit' in request.POST:
            edit_phone_id = request.POST['edit_phone_id']
            phone_to_edit = ClientPhoneNumber.objects.get(pk=edit_phone_id)
            edit_form = ClientPhoneNumberForm(request.POST, instance=phone_to_edit)
            if edit_form.is_valid():
                edit_form.save()
                del edit_form
                edit_phone_id = None
        if 'choose_edit' in request.POST:
            user_phone_id = request.POST['edit_phone_id']
            phone_to_edit = ClientPhoneNumber.objects.get(pk=user_phone_id)
            edit_form = ClientPhoneNumberForm(instance=phone_to_edit)
            edit_phone_id = user_phone_id

    try:
        new_phone_form
    except:
        new_phone_form = ClientPhoneNumberForm()

    try:
        edit_form
    except:
        edit_form = ClientPhoneNumberForm()

    phones = client.clientphonenumber_set.all()

    return render_to_response('add_phone.templ',
                              {'new_phone_form': new_phone_form,
                               'edit_form': edit_form,
                               'phones': phones,
                               'edit_phone_id': edit_phone_id,
                               'client_id': client_id},
                               context_instance=RequestContext(request))
