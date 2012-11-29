#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from clients.models import Client, ClientPhoneNumber, Address
from clients.forms import NaturalClientForm, LegalClientForm, AddressForm, ClientPhoneNumberForm


def clients(request):
    """
    """
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
    return render_to_response('client.templ',
                              {'client': client},
                               context_instance=RequestContext(request))


def create_client(request, client_type):
    """
    """
    if client_type == "natural":
        form_class = NaturalClientForm
    elif client_type == "legal":
        form_class = LegalClientForm
    else:
        raise Exception("Error en el URL")

    if request.method == 'POST':
        client_form = form_class(request.POST)

        if client_form.is_valid():
            print "Client is valid"
            new_client = client_form.save(commit=False)
            new_client.created_by = request.user
            new_client.modified_by = request.user
            new_client.save()
            print "Client saved"
            return HttpResponseRedirect(reverse('clients.views.client', kwargs={'client_id': new_client.id}))
        else:
            print "Its not valid"
    else:
        client_form = form_class()

    return render_to_response('create_client.templ',
                              {'client_form': client_form, },
                               context_instance=RequestContext(request))


def create_address(request, client_id):
    """
    """
    # import pdb; pdb.set_trace()
    client = Client.objects.get(pk=client_id)
    if client.address:
        instance = client.address
    else:
        instance = Address()

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
