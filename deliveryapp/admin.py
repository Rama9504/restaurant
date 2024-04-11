from django.contrib import admin

# Register your models here.
from django.contrib import admin

from deliveryapp.models import deliverdetails
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(deliverdetails,ImportExportModelAdmin)
