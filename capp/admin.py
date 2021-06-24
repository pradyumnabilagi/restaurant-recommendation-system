from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(UserModel)
admin.site.register(restaurant)
admin.site.register(menu)
admin.site.register(order)
admin.site.register(cart)