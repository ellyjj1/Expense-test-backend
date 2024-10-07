from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions.views import TransactionViewSet, register, UserViewSet  # 添加 UserViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'users', UserViewSet, basename='user')  # 注册新的用户视图集

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', obtain_auth_token),
    path('register/', register),
    path('', TemplateView.as_view(template_name='index.html'), name='home')
]
