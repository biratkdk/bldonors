from django.contrib import admin
from .models import Bloodreq, Contact, Donor, Payment, Stock


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_group", "quantity", "phone", "email")
    search_fields = ("name", "email", "blood_group")


@admin.register(Bloodreq)
class BloodreqAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_group", "quantity", "phone", "email")
    search_fields = ("name", "email", "blood_group")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_group", "quantity", "phone", "email")
    search_fields = ("name", "email", "blood_group")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email")
    search_fields = ("name", "email", "subject")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("donor_name", "amount", "purpose", "payment_method", "status", "transaction_id")
    search_fields = ("donor_name", "email", "transaction_id", "purpose")
