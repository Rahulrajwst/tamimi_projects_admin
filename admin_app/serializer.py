from rest_framework import serializers
from .models import CategoryInfoModel

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoryInfoModel
        fields=('catid','categoryname','handle','categoryhomeimage','categorysectionimage')
