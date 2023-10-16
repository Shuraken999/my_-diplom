from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from inetshop.models import Product, Shop
from inetshop.serializers import ProductSerializer


# Create your views here.

class ProductView(APIView):

    def get(self, request, *args, **kwargs):
        shop = Shop.objects.create(name='Shop 1', state=True)
        Product.objects.create(name='Product 1',
                                          category='Category 1',
                                          quantity=10,
                                          price=10,
                                          shop_id=shop.id)
        products = Product.objects.all().select_related('shop')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
