

from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeRecordViewSet

router = DefaultRouter()
router.register(r"fees", FeeRecordViewSet, basename="feerecord")
urlpatterns = [
    path("api/", include(router.urls)),
    path('', views.fee_list, name='fee_list'),
    path('create/', views.fee_create, name='fee_create'),
    path('edit/<int:pk>/', views.fee_edit, name='fee_edit'),
    path('delete/<int:pk>/', views.fee_delete, name='fee_delete'),
    path('voucher/<int:pk>/', views.fee_voucher, name='fee_voucher'),
]
