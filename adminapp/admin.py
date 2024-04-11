from django.contrib import admin
from adminapp.models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(adminss,ImportExportModelAdmin)
admin.site.register(dishes,ImportExportModelAdmin)
admin.site.register(orders,ImportExportModelAdmin)
admin.site.register(deliveryboys,ImportExportModelAdmin)
#admin.site.register(carts,ImportExportModelAdmin)
#admin.site.register(deliverymapping,ImportExportModelAdmin)
admin.site.register(cartprice,ImportExportModelAdmin)
admin.site.register(deliverymappings,ImportExportModelAdmin)
admin.site.register(orderverif,ImportExportModelAdmin)
admin.site.register(deliverymappingss,ImportExportModelAdmin)
admin.site.register(Review,ImportExportModelAdmin)
admin.site.register(order,ImportExportModelAdmin)