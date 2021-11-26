from django.urls import path, include
from .views import *

urlpatterns = [
    path('activate_register/', ActivateRegisterUser.as_view(), name="activate_register"),
    path('activate_fast_register/', ActivateFastRegisterUser.as_view(), name="activate_fast_register"),
    path('authenticate/', AuthenticationUser.as_view(), name="authenticate"),
    path('admin_authenticate/', AuthenticationAdmin.as_view(), name="admin_authenticate"),
    path('start_register/', StartRegisterUser.as_view(), name="start_register"),
    path('start_fast_register/', StartFastRegisterUser.as_view(), name="start_fast_register"),
    path('start_reset_password/', StartResetPassword.as_view(), name="start_reset_password"),
    path('finish_reset_password/', FinishResetPassword.as_view(), name="finish_reset_password"),
    
    path('order/', FormOrder.as_view(), name="order"),
]

app_name = 'account'
