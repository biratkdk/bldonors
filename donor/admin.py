from django.contrib import admin
from .models import Donor , Bloodreq , Stock ,Contact 

# Register your models here.
admin.site.register(Donor)
admin.site.register(Bloodreq)
admin.site.register(Stock)
admin.site.register(Contact)
