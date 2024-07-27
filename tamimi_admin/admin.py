from django.contrib import admin
from . models import CategoryModel,DeviceModel,SectionModel,ParentSectionModel
# Register your models here.

admin.site.register(DeviceModel)
admin.site.register(SectionModel)
admin.site.register(ParentSectionModel)
admin.site.register(CategoryModel)