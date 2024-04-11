from django.contrib import admin
from sapp.models import UserProfile,Location
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(UserProfile,ImportExportModelAdmin)
admin.site.register(Location,ImportExportModelAdmin)