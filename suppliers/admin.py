from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from suppliers.models import Supplier, Product
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'level', 'prev_supplier_link',)
    list_filter = ('city',)
    exclude = ('level',)
    actions = ['clear_debt']

    @admin.display(description="ссылка на поставщика")
    def prev_supplier_link(self, obj):
        if obj.prev_supplier_id:
            my_reverse = reverse("admin:suppliers_supplier_change", args=(obj.prev_supplier_id,))
            return mark_safe(f'<a href="{my_reverse}">{obj.prev_supplier}</a>')
        else:
            return None

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0.00)
        self.message_user(
            request,
            ngettext(
                "%d задолженность поставщика была успешно погашена",
                "%d задолженности поставщиков были успешно погашены",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


    def save_model(self, request, obj, form, change):
        #Перед сохранением вычисляет длину иерархии

            level = 0
            prev_supplier_id = obj.prev_supplier_id
            while prev_supplier_id:
                level += 1
                next_prev_supplier = Supplier.objects.get(pk=prev_supplier_id)
                print(next_prev_supplier.prev_supplier_id)

                if next_prev_supplier.prev_supplier_id is not None:
                    prev_supplier_id = next_prev_supplier.prev_supplier_id
                else:
                    prev_supplier_id = None
                    obj.level = level

            else:
                obj.level = level
            #проверка не вышла ли длина иерархии за пределы критерия
            try:
                if level > 2:
                    raise ValidationError("Длина звена цепи должен быть не больше 3 участников")
                else:
                    super(SupplierAdmin, self).save_model(request, obj, form, change)
            except ValidationError as err:
                messages.set_level(request, messages.ERROR)
                self.message_user(request, err.message, level=messages.ERROR)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_model', 'release_date',)
