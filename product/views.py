from rest_framework.views import APIView
from rest_framework.response import Response

import json
from product.models import Product
from datetime import datetime
import re
from product.serializers import ProductSerializer
from rest_framework import status


class ProductsSearch(APIView):
    """
    Search products
    """

    def get(self, request):
        keyword = request.GET.get('keyword', None)
        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)

        if not keyword:
            return Response({'message': 'Invalid search conditions'}, status=status.HTTP_400_BAD_REQUEST)

        products_qs = Product.objects.filter(name__icontains=keyword)

        if min_price:
            products_qs = products_qs.filter(price__gt=min_price)

        if max_price:
            products_qs = products_qs.filter(price__lt=max_price)

        data = ProductSerializer(products_qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ProductsList(APIView):
    """
    View to list all products
    """

    def get(self, request):
        products_qs = Product.objects.all()
        data = ProductSerializer(products_qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


def valid_product_name(product_name):
    """
    Validate product name
    Name for the product, 4-10 characters long. The first letter has to be a digit or a letter (0-9, A-Z, a-z).
    All other letters has to be a digit, a letter, a space, or a hyphen (0-9, A-Z, a-z, , -).
    :param product_name:
    :return:
    """
    pattern = "^[0-9A-Za-z][0-9A-Za-z -]*$"
    matched = re.match(pattern, product_name)
    return bool(matched)


def validate_products_data(products):
    """
    Validate inputs products data
        - Name, price, start_date exists
        - Name should not already taken
        - Start date should not past date
    :param products:
    :return:
    """
    invalid_products = [product for product in products if
                        product['start_date'] == ''
                        or datetime.strptime(product.get('start_date', '01/01/1990'), '%m/%d/%Y') <= datetime.now()
                        or product.get('price', '') == '' or not isinstance(product.get('price', ''), int)
                        or product.get('name', '') == '' or not valid_product_name(product.get('name', ''))]

    if len(invalid_products) > 0:
        print("invalid inputs")
        return False

    product_names = [product.get('name', '') for product in products]
    products = Product.objects.filter(name__in=product_names)
    if len(products) > 0:
        return False

    return True


class ProductAdd(APIView):
    def post(self, request):
        products = {}

        try:
            input_data = json.loads(request.body)
            products = input_data['posts']
        except Exception as exc:
            pass

        if products and validate_products_data(products):
            for product in products:
                product['start_date'] = datetime.strptime(product.get('start_date'), '%m/%d/%Y').date()
                Product.objects.create(**product)

            status_code = status.HTTP_201_CREATED
            message = f'{len(products)} Product(s) added successfully'
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            message = 'Failed to load products'

        return Response({'message': message}, status=status_code)
