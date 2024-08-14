from typing import Any
from django.db import models

# Create your models here.


class CategoryModel(models.Model):

    catid=models.CharField(max_length=250, editable=False)
    categoryname=models.CharField(max_length=250, editable=False)
    handle=models.CharField(max_length=250, editable=False)
    def __str__(self):
        return self.categoryname

    
class DeviceModel(models.Model):
    category=models.ForeignKey(CategoryModel, null=True, on_delete=models.CASCADE)
    deviceimage=models.ImageField(upload_to='deviceimages/', null=True, blank=True)
    def __str__(self):
        return self.category.categoryname
    
    
class ParentSectionModel(models.Model):
    parentsectionname=models.CharField(max_length=250)
    parentsectionimage=models.ImageField(upload_to='parentsectionimages/')
    def __str__(self):
        return self.parentsectionname
    

class SectionModel(models.Model):
    category=models.ForeignKey(CategoryModel,null=True, on_delete=models.CASCADE)
    sectionimage=models.ImageField(upload_to='sectionimages/', null=True, blank=True)
    parentsection=models.ForeignKey(ParentSectionModel, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.category.categoryname
    
class DeviceOrderModel(models.Model):
    sortno=models.IntegerField()
    device=models.OneToOneField(DeviceModel, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.device.category.categoryname
    

class SectionOrderModel(models.Model):
    sortno=models.IntegerField()
    parent=models.BooleanField()
    parentsection=models.OneToOneField(ParentSectionModel, null=True, on_delete=models.CASCADE)
    normalsection=models.OneToOneField(SectionModel, null=True, on_delete=models.CASCADE)
    def __str__(self):
        if self.parent:
            return self.parentsection.parentsectionname
        else:
            return self.normalsection.category.categoryname
        


class FCMTokenModel(models.Model):
    device_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

