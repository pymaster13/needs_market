from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone


class Adress(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=20, verbose_name='Дом')
    flat = models.CharField(max_length=20, verbose_name='Квартира', blank = True, null = True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.city


class Card(models.Model):
    number = models.CharField(max_length=30, verbose_name='Номер карты')
    date = models.DateField(verbose_name='Дата активности')
    owner = models.CharField(max_length=100, verbose_name='Владелец карты')

    class Meta:
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'

    def __str__(self):
        return self.number


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Наименование категории')
    category_image = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name


class Good(models.Model):
    good_name = models.CharField(max_length=100, verbose_name='Наименование товара')
    good_image = models.ImageField(blank=True, null=True)
    price = models.CharField(max_length=100, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', verbose_name='Категория')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.good_name


class GoodCount(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='good', verbose_name='Наименование товара')
    count = models.FloatField(verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    def __str__(self):
        return self.good.good_name


class Status(models.Model):
    status_name = models.CharField(max_length=100, verbose_name='Статус заказа')

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'

    def __str__(self):
        return self.status_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_comment', verbose_name='Заказчик')
    comment = models.CharField(max_length=5000, verbose_name='Пожелание')

    class Meta:
        verbose_name = 'Пожелание'
        verbose_name_plural = 'Пожелания'

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', verbose_name='Заказчик')
    good = models.ManyToManyField(GoodCount, related_name='good_name', verbose_name='Заказанный товар')
    total_price = models.FloatField(verbose_name='Общая сумма заказа')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status', verbose_name='Статус заказа')
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE, related_name='adress_city', verbose_name='Адрес доставки')
    date = models.DateTimeField(editable = True, blank = True, null = True, verbose_name='Дата доставки')
    time = models.DateTimeField(editable = True, blank = True, null = True, verbose_name='Время доставки')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_goods(self):
        good_list = self.good.get_queryset()
        goods_str = ''
        for good in good_list:
            goods_str += ', ' + str(good)
        return goods_str.lstrip(', ')    
    get_goods.short_description = 'Заказанные товары'

    def get_goods_all(self):
        good_list = self.good.get_queryset()
        goods = []
        for good in good_list:
            good_id = Good.objects.get(good_name = good).id
            goods.append({'id': good_id, 'good_name': str(good), 'count': good.count, 'price': good.price})
        return goods
    get_goods_all.short_description = 'Заказанные товары с параметрами'

    def get_phone(self):
        user_phone = self.user.username
        return str(user_phone)
    get_phone.short_description = 'Номер заказчика'

    def get_firstname(self):
        user_firstname = self.user.first_name
        return str(user_firstname)
    get_firstname.short_description = 'Имя заказчика'

    def get_status(self):
        status = self.status.status_name
        return str(status)
    get_status.short_description = 'Статус заказа'

    def get_adress(self):
        country = self.adress.country
        city = self.adress.city
        street = self.adress.street
        house = self.adress.house
        flat = self.adress.flat
        adr = "%s, г. %s, ул. %s, д. %s, кв. %s" % (country, city, street, house, flat)
        return str(adr)
    get_status.short_description = 'Адрес доставки'

    def __str__(self):
        return self.user.username
