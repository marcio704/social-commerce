from django.contrib import admin

# Register your models here.

from .models import Store, Vendor, Product, Brand, Post, Clooset

admin.site.register(Store)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Post)
admin.site.register(Clooset)
