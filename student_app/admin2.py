import csv
from django.contrib import admin
from django.http import HttpResponse
from django import forms
from .models import Student

from import_export.admin import ImportExportModelAdmin

class RecordAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'about', 'pub_date')
    list_display_links = ('name', 'email', 'about', 'pub_date')
    search_fields = ('name', 'email', 'about')
    list_per_page = 25

# Form for CSV upload
class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(label="Select a CSV file")

    # Register your models here.
admin.site.register(Student, ImportExportModelAdmin)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'about', 'pub_date') #fields to display
    actions = ['download_selected_as_csv'] #add download action
    change_list_template = 'admin/student_app/student/change_list.html' #Custom template for upload button

#Action to download selected records as CSV
    def download_selected_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        # Write header
        writer.writerow(['Name', 'Email', 'About', 'Publication Date'])

        # Write date for selected products
        for student in queryset:
            writer.writerow([student.name, student.email, student.about, student.pub_date])
        return response
    download_selected_as_csv.short_description = 'Download selected as CSV'
#Handle CSV upload
def change_list_view(self, request, extra_context=None):
    if request.method  == 'POST' and 'upload_csv' in request.POST:
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Student.objects.update_or_create(
                    student_code=row['student_code'],
                    defaults={
                    'name': row['name'],
                    'email': row['email'],
                    'about': row['about'],
                    'pub_date': row['pub_date']})
                    
            self.message_user(request, 'CSV file uploaded successfully')

    else:
        form = CsvUploadForm()

    extra_context = extra_context or {}
    extra_context['csv_upload_form'] = form
    return super().change_list_view(request, context=extra_context)