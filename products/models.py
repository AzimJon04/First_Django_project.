from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Genres"
        verbose_name = "Genre"
        ordering = ['name']


class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    price = models.FloatField()
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    stock = models.IntegerField()
    data_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Books"
        verbose_name = "Book"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    data_created = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def sum(self):
        return self.quantity * self.product.price


class OrdersQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(order.sum() for order in self)

    def total_quantity(self):
        return sum(order.quantity for order in self)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    data_created = models.DateTimeField(auto_now_add=True)

    objects = OrdersQuerySet.as_manager()

    def sum(self):
        return self.quantity * self.product.price
