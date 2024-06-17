from django.contrib import admin

# Register your models here.
from . models import *
admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','user_received']
    model = Order

