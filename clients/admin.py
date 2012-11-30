from clients.models import NaturalClient, LegalClient, Referrer, ClientAddress, ClientPhoneNumber
from django.contrib import admin

admin.site.register(LegalClient)
admin.site.register(NaturalClient)
admin.site.register(Referrer)
admin.site.register(ClientAddress)
admin.site.register(ClientPhoneNumber)
