from django.contrib import admin

# Register your models here.

from .models import SearchHistory, Shop

admin.site.register(SearchHistory)
admin.site.register(Shop)