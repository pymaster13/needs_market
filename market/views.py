import datetime
from datetime import datetime as dt

from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *

class OrderView(viewsets.ModelViewSet):
    """
    A simple ViewSet that for listing or retrieving users.
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def list(self, request):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):
            queryset = Order.objects.all()
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response({'auth' : 'error'})

    def retrieve(self, request, pk=None):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):
            queryset = Order.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = OrderSerializer(user)
            return Response(serializer.data)

        return Response({'auth' : 'error'})

class CategoryView(viewsets.ModelViewSet):
    """
    A simple ViewSet that for listing or retrieving users.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):
            queryset = Category.objects.all()
            serializer = CategorySerializer(queryset, many=True)
            return Response(serializer.data)

        return Response({'auth' : 'error'})

    def retrieve(self, request, pk=None):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):
            queryset = Category.objects.all()
            category = get_object_or_404(queryset, pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        return Response({'auth' : 'error'})

class GoodView(viewsets.ModelViewSet):
    """
    A simple ViewSet that for listing or retrieving users.
    """

    serializer_class = GoodSerializer
    queryset = Good.objects.all()

    def list(self, request):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):
            queryset = Good.objects.all()
            serializer = GoodSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response({'auth' : 'error'})

    def retrieve(self, request, pk=None):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):
            queryset = Good.objects.all()
            good = get_object_or_404(queryset, pk=pk)
            serializer = GoodSerializer(good)
            return Response(serializer.data)

        return Response({'auth' : 'error'})

class UserCategoryView(APIView):
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data})

class UserGoodView(APIView):
    
    def get(self, request, pk=None):
        goods = Good.objects.filter(category = Category.objects.get(pk=pk))
        serializer = UserGoodSerializer(goods, many=True)
        return Response({"goods": serializer.data})

class UserCommentsView(APIView):
    
    def get(self, request):
        comments = Comment.objects.all()
        serializer = UserCommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})

    def post(self, request, format=None):
        try:
            user = Token.objects.get(key = request.headers['Authorization'][7::]).user
            comment_add = {'comment' : request.data['comment'], 'user' : user.id}
            serializer = UserCommentSerializer(data=comment_add)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            user = User.objects.get(username = 'Аноним')
            comment_add = {'comment' : request.data['comment'], 'user' : user.id}
            serializer = UserCommentSerializer(data=comment_add)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatUsersView(APIView):

    def get(self, request, pk=None):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):

            if pk == 'week':
                today = dt.today()
                last_week = today - datetime.timedelta(days=7)
                users_week = User.objects.filter(date_joined__range=(last_week, today))
                return Response({"count_users": users_week.count()})

            elif pk == 'month':
                now_month = dt.today().month
                a = User.objects.all().annotate(month=TruncMonth("date_joined")) \
                    .values("month").annotate(c=Count("id")).order_by("-month")

                for one_month in a:
                    if one_month['month'].month == now_month:
                        return Response({"count_users": one_month['c']})
                
                return Response({"count_users": '0'})

            elif pk == 'year':
                now_year = dt.today().year
                a = User.objects.all().annotate(year=TruncYear("date_joined")) \
                    .values("year").annotate(c=Count("id")).order_by("-year")
                
                for one_year in a:
                    if one_year['year'].year == now_year:
                        return Response({"count_users": one_year['c']})
                return Response({"count_users": '0'})
        
        return Response({'auth' : 'error'})

class StatOrdersView(APIView):
    
    def get(self, request, pk=None):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):

            if pk == 'week':
                today = dt.today()
                last_week = today - datetime.timedelta(days=7)
                orders_week = Order.objects.filter(date__range=(last_week, today))
                return Response({"count_orders": orders_week.count()})

            elif pk == 'month':
                now_month = dt.today().month
                a = Order.objects.all().annotate(month=TruncMonth("date")) \
                    .values("month").annotate(c=Count("id")).order_by("-month")
                
                for one_month in a:
                    if one_month['month'].month == now_month:
                        return Response({"count_orders": one_month['c']})
                
                return Response({"count_orders": '0'})

            elif pk == 'year':
                now_year = dt.today().year
                a = Order.objects.all().annotate(year=TruncYear("date")) \
                    .values("year").annotate(c=Count("id")).order_by("-year")
                
                for one_year in a:
                    if one_year['year'].year == now_year:
                        return Response({"count_orders": one_year['c']})
                return Response({"count_orders": '0'})
        
        return Response({'auth' : 'error'})

class StatGoodsView(APIView):
    
    def get(self, request, pk=None):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):
            current_good = GoodCount.objects.filter(good = Good.objects.get(pk=pk))
            month_good = []
            now_year = dt.today().year
            a = current_good.annotate(month=TruncMonth("date")).values("month").annotate(c=Count("id")).order_by("-month")
            
            for one_month in a:
                if one_month['month'].year == now_year:
                    month_good.append({'name' : one_month['month'].month, 'количество' : one_month['c']})
            true_month_good = sorted(month_good, key=lambda x: x['name'])
            return Response(true_month_good)

        return Response({'auth' : 'error'})

class StatGoodsAllView(APIView):

    def get(self, request):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):
            month_good = []
            now_year = dt.today().year
            a = GoodCount.objects.all().annotate(month=TruncMonth("date")).values("month") \
                .annotate(c=Count("id")).order_by("-month")
    
            for one_month in a:
                if one_month['month'].year == now_year:
                    month_good.append({'name' : one_month['month'].month, 'количество' : one_month['c']})

            true_month_good = sorted(month_good, key=lambda x: x['name'])
            return Response(true_month_good)

        return Response({'auth' : 'error'})

class StatTopView(APIView):

    def get(self, request, pk=None):
        if request.headers['Authorization'] == 'Bearer ' + str(Token.objects.get(user = 1)):

            if pk == 'week':
                top_week_goods = []
                today = dt.today()
                last_week = today - datetime.timedelta(days=7)
                orders_week = GoodCount.objects.filter(date__range=(last_week, today))
                top = orders_week.values('good').annotate(c = Count('good')).order_by("-c")

                for one_top in top[:5]:
                    top_week_goods.append({'name' : str(Good.objects.get(pk = one_top['good'])), 'количество' : one_top['c']})

                return Response(top_week_goods)

            elif pk == 'month':
                top_month_good = []
                now_year = dt.today().year
                now_month = dt.today().month
                top = GoodCount.objects.all().annotate(month=TruncMonth("date")) \
                    .values("good", "month").annotate(c = Count("good")).order_by("-c")

                for one_top in top:
                    if one_top['month'].year == now_year:
                        if one_top['month'].month == now_month:
                            top_month_good.append({'name' : str(Good.objects.get(pk = one_top['good'])), 'количество' : one_top['c']})
                            if len(top_month_good) == 5:
                                break

                return Response(top_month_good)

            elif pk == 'year':
                top_year_good = []
                now_year = dt.today().year
                top = GoodCount.objects.all().annotate(year=TruncYear("date")) \
                    .values("good", "year").annotate(c = Count("good")).order_by("-c")

                for one_top in top:
                    if one_top['year'].year == now_year:
                        top_year_good.append({'name' : str(Good.objects.get(pk = one_top['good'])), 'количество' : one_top['c']})
                        if len(top_year_good) == 5:
                            break
                return Response(top_year_good)

        return Response({'auth' : 'error'})

class UserOrdersView(APIView):

    def get(self, request):
        serializer_class = OrderSerializer
        user = Token.objects.get(key = request.headers['Authorization'][7::]).user
        user_orders = Order.objects.filter(user = user)
        serializer = OrderSerializer(user_orders, many=True)
        return Response(serializer.data)

class SearchGoodsAllView(APIView):

    def get(self, request):
        serializer_class = GoodSerializer
        searched_goods = Good.objects.all()
        serializer = GoodSerializer(searched_goods, many=True)
        return Response(serializer.data)

class SearchGoodsView(APIView):

    def get(self, request, pk=None):
        serializer_class = GoodSerializer
        searched_goods = Good.objects.filter(good_name__istartswith = pk)
        serializer = GoodSerializer(searched_goods, many=True)
        return Response(serializer.data)

class SearchCategoriesAllView(APIView):

    def get(self, request, pk=None):
        serializer_class = CategorySerializer
        searched_categories = Category.objects.all()
        serializer = CategorySerializer(searched_categories, many=True)
        return Response(serializer.data)

class SearchCategoriesView(APIView):

    def get(self, request, pk=None):
        serializer_class = CategorySerializer
        searched_categories = Category.objects.filter(category_name__istartswith = pk)
        serializer = CategorySerializer(searched_categories, many=True)
        return Response(serializer.data)
