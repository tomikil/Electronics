from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from suppliers.models import Supplier, Product


class SupplierSerializer(serializers.ModelSerializer):
    """Сериализатор поставщика """

    class Meta:
        model = Supplier
        exclude = ('level',)

    def create(self, validated_data):
        level = 0
        prev_supplier_id = self.validated_data['prev_supplier'].pk
        print(prev_supplier_id)
        while (prev_supplier_id):
            level += 1
            next_supplier = Supplier.objects.get(pk=prev_supplier_id)
            print(next_supplier)
            if level > 2:
                print(level)
                raise ValidationError("Длина звена цепи должен быть не больше 3 участников")
            if next_supplier is not None:
                prev_supplier_id = next_supplier.prev_supplier_id

            else:
                prev_supplier_id = None
        else:
            return Supplier.objects.create(**self.validated_data)


class SupplierSerializerUpdate(serializers.ModelSerializer):
    """Сериализатор поставщика для редактирования """
    class Meta:
        model = Supplier
        exclude = ('debt', 'created_at', 'level')

class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор Продукта"""

    class Meta:
        model = Product
        fields = '__all__'
