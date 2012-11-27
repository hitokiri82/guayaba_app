from clients.models import NaturalClient, LegalClient, Referrer, Address, ClientPhoneNumber
from django.contrib import admin

admin.site.register(LegalClient)
admin.site.register(NaturalClient)
admin.site.register(Referrer)
admin.site.register(Address)
admin.site.register(ClientPhoneNumber)
