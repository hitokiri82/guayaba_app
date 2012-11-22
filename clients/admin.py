from clients.models import NaturalClient, LegalClient, Referrer
from django.contrib import admin

admin.site.register(LegalClient)
admin.site.register(NaturalClient)
admin.site.register(Referrer)
