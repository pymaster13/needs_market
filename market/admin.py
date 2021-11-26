from django.contrib import admin
from .models import *

admin.site.register(Status)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',
    'category_name',
    'category_image',)

@admin.register(Adress)
class AdressAdmin(admin.ModelAdmin):
    list_display = ('city',
    'street',
    'house',
    'flat',)

    list_filter = ('street',)
    search_fields = ('city', 'street',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('number',
    'date',
    'owner',)

    search_fields = ('number', 'owner',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id',
    'user',
    'comment',)

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('good_name',
    'price',
    'category',)

    list_filter = ('good_name', 'category',)
    search_fields = ('good_name', 'price', 'category',)

@admin.register(GoodCount)
class GoodCountAdmin(admin.ModelAdmin):
    list_display = ('good',
    'count',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',
    'get_goods',
    'total_price',
    'status',
    'adress',
    'date',)

    search_fields = ('user', 'status',)
