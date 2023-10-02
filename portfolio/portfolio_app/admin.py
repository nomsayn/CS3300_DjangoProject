from django.contrib import admin
from .models import Student, Portfolio

# Register your models here so they can be edited in admin panel
admin.site.register(Student)
admin.site.register(Portfolio)
