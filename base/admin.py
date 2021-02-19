from django.contrib import admin

# Register your models here.
from base.models import Photo, CategoryPhoto

admin.site.register([Photo])
admin.site.register([CategoryPhoto])
