from django.db.models import Count
from rest_framework import serializers

from .models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'get_phone', 'get_firstname', 'get_goods_all',
            'total_price', 'status', 'get_status', 'get_adress', 'date')


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ('id', 'good_name', 'good_image', 'price', 'category')

class CategorySerializer(serializers.ModelSerializer):
    goods = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'category_name', 'category_image', 'goods')

    def get_goods(self, obj):
        try:
            category = Category.objects.filter(id = obj.id).annotate(num_goods=Count('category'))
            count_goods = category[0].num_goods
            return count_goods
        except:
            return 0

class UserCommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.first_name', read_only=True)
    phone = serializers.ReadOnlyField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'phone', 'comment')

class UserCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_name = serializers.CharField(max_length=120)
    category_image = serializers.CharField()

class UserGoodSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    good_name = serializers.CharField(max_length=120)
    good_image = serializers.ImageField()
    price = serializers.CharField()
    category = serializers.CharField()
