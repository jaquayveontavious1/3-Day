from django.contrib import admin

# Register your models here.

from .models import Sprint, Goal

admin.site.register(Sprint)
admin.site.register(Goal)