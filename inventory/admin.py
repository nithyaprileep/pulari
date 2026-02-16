
from django.contrib import admin
from .models import Customer, Feed, Supplier, Purchase, Sale

admin.site.register(Supplier)
admin.site.register(Feed)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Customer)