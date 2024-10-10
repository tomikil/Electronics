from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework import generics

from suppliers.models import Supplier, Product
from suppliers.permissions import IsActive
from suppliers.serializers import SupplierSerializer, SupplierSerializerUpdate, ProductSerializer


class SupplierCreateAPIView(generics.CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsActive,)

    def perform_create(self, serializer):
        supplier = serializer.save()
        level = 0
        prev_supplier_id = supplier.prev_supplier_id
        while prev_supplier_id:
            level += 1
            next_prev_supplier = Supplier.objects.get(pk=prev_supplier_id)
            if next_prev_supplier is not None:
                prev_supplier_id = next_prev_supplier.prev_supplier_id
            else:
                supplier.level = level
        else:
            supplier.level = level
        supplier.save()


class SupplierRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsActive,)


class SupplierUpdateAPIView(generics.UpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializerUpdate
    permission_classes = (IsActive,)


class SupplierListAPIView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsActive,)
    filter_backends = (SearchFilter,)
    search_fields = ['country']


class SupplierDestroyAPIView(generics.DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsActive,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsActive,)
