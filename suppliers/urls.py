from rest_framework.routers import SimpleRouter
from django.urls import path
from suppliers.apps import SuppliersConfig
from suppliers import views


app_name = SuppliersConfig.name

router = SimpleRouter()
router.register(r"product", views.ProductViewSet, basename='product')


urlpatterns = [
    path('suppliers/list/', views.SupplierListAPIView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateAPIView.as_view(), name='supplier_create'),
    path('suppliers/detail/<int:pk>/', views.SupplierRetrieveAPIView.as_view(), name='supplier_detail'),
    path('suppliers/update/<int:pk>', views.SupplierUpdateAPIView.as_view(), name='supplier_update'),
    path('suppliers/delete/<int:pk>', views.SupplierDestroyAPIView.as_view(), name='supplier_delete'),
] + router.urls