import csv
from django.contrib import admin
from .models import Student

from import_export.admin import ImportExportModelAdmin

class RecordAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'about', 'pub_date')
  


# Register your models here.
admin.site.register(Student, ImportExportModelAdmin)
