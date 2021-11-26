from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'market'

router = DefaultRouter()
router.register(r'admin/orders', OrderView, basename='order')
router.register(r'admin/categories', CategoryView, basename='category')
router.register(r'admin/goods', GoodView, basename='good')

urlpatterns = [
    path('admin/statistic/users/<str:pk>/', StatUsersView.as_view()),
    path('admin/statistic/orders/<str:pk>/', StatOrdersView.as_view()),
    path('admin/statistic/goods/<int:pk>/', StatGoodsView.as_view()),
    path('admin/statistic/goods/all/', StatGoodsAllView.as_view()),
    path('admin/statistic/top/<str:pk>/', StatTopView.as_view()),

    path('categories/', UserCategoryView.as_view()),
    path('categories/<int:pk>/', UserGoodView.as_view()),
    
    path('search/goods/', SearchGoodsAllView.as_view()),
    path('search/goods/<str:pk>/', SearchGoodsView.as_view()),
    path('search/categories/', SearchCategoriesAllView.as_view()),
    path('search/categories/<str:pk>/', SearchCategoriesView.as_view()),
    
    path('user/orders/', UserOrdersView.as_view()),
    path('user/comments/', UserCommentsView.as_view()),
]

urlpatterns += router.urls