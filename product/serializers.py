from rest_framework import serializers
from product.models import Product
from datetime import datetime


class ProductSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()

    @staticmethod
    def get_start_date(obj):
        return datetime.strftime(obj.start_date, '%m/%d/%Y')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'start_date']
