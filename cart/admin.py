from django.contrib import admin
from .models import Order, Item, CheckoutFeedback

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(CheckoutFeedback)
