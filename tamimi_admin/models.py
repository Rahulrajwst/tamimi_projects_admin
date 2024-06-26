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
    category=models.ForeignKey(CategoryModel, null=True, on_delete=models.SET_NULL)
    deviceimage=models.ImageField(upload_to='deviceimages/', null=True, blank=True)
    def __str__(self):
        return self.category.categoryname
    
    
class ParentSectionModel(models.Model):
    parentsectionname=models.CharField(max_length=250)
    parentsectionimage=models.ImageField(upload_to='parentsectionimages/')
    def __str__(self):
        return self.parentsectionname
    

class SectionModel(models.Model):
    category=models.ForeignKey(CategoryModel,null=True, on_delete=models.SET_NULL)
    sectionimage=models.ImageField(upload_to='sectionimages/', null=True, blank=True)
    parentsection=models.ForeignKey(ParentSectionModel, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.category.categoryname