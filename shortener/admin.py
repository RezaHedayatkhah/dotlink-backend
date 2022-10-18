from django.contrib import admin

from shortener.models import Link, Location

# Register your models here.
admin.site.register(Link)
admin.site.register(Location)