from django.db import models


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=300, verbose_name='Название продукта')
    product_model = models.CharField(max_length=100, verbose_name='Модель продукта')
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок')

    def __str__(self):
        return f'{self.name}, модель: {self.product_model}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Supplier(models.Model):
    """Модель поставщика"""
    name = models.CharField(max_length=200, verbose_name='Название')
    email = models.EmailField(verbose_name='email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=150, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукты',
                                related_name='Product', blank=True, null=True)
    prev_supplier = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name='Поставщик',
                                      related_name='prev', blank=True, null=True)
    level = models.IntegerField(verbose_name='Уровень иерархии', blank=True, null=True)
    debt = models.DecimalField(max_digits=20, decimal_places=2, default=0.00,
                               verbose_name='Задолженность перед поставщиком')
    created_at = models.DateField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.name}, продукт: {self.product.name}'

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['country']
