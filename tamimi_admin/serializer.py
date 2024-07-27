from rest_framework import serializers
from .models import DeviceModel,CategoryModel,SectionModel,ParentSectionModel,DeviceOrderModel,SectionOrderModel

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CategoryModel
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model=DeviceModel
        fields='__all__'

class DeviceOrderSerializer(serializers.ModelSerializer):
    device = DeviceSerializer()
    class Meta:
        model=DeviceOrderModel
        fields='__all__'   




class ParentSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ParentSectionModel
        fields='__all__'

class SectionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    parentsection = ParentSectionSerializer()
    class Meta:
        model=SectionModel
        fields='__all__'

class SectionOrderSerializer(serializers.ModelSerializer):
    normalsection = SectionSerializer()
    parentsection = ParentSectionSerializer()
    class Meta:
        model=SectionOrderModel
        fields='__all__' 

    
    # class Meta:
    #     model=CategoryModel
    #     fields="__all__"
    # def to_representation(self, instance):
    #     representation = dict()
    #     representation["id"] = instance.id
    #     representation["name"] = instance.category.categoryname # see this
    #     representation["catid"] = instance.category.catid
    #     representation["handle"] = instance.category.handle
    #     representation["image"] = instance.deviceimage
    #     return representation
