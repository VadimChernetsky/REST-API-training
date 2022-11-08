from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accounting import views


app_name = 'accounting'

router = DefaultRouter()

router.register('auser', views.AUserDetail2)
router.register('account', views.AccountViewSet)
router.register('action', views.ActionViewSet)
router.register('transaction', views.TransactionViewSet)
router.register('category', views.CategorySerializer)

urlpatterns = [
    path('', include(router.urls)),
    path('auser/', views.AUserDetail3.as_view(), name='customer'),
]
