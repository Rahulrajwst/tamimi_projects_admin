from django.contrib import admin
from . models import CategoryInfoModel,DeviceModel

# Register your models here.

admin.site.register(CategoryInfoModel)
admin.site.register(DeviceModel)