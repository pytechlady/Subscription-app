from django.contrib import admin
from .models import Company, Subscription

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "company_identifier", "email")
admin.site.register(Company, CompanyAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "subscription_name", "amount")
admin.site.register(Subscription, SubscriptionAdmin)