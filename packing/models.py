from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    length = models.FloatField(validators=[MinValueValidator(0.01)])  # cm
    width = models.FloatField(validators=[MinValueValidator(0.01)])   # cm
    height = models.FloatField(validators=[MinValueValidator(0.01)])  # cm
    weight = models.FloatField(validators=[MinValueValidator(0.01)])  # kg

    def __str__(self):
        return self.name

    @property
    def volume(self):
        return self.length * self.width * self.height


class Box(models.Model):
    name = models.CharField(max_length=255)
    inner_length = models.FloatField(validators=[MinValueValidator(0.01)])  # cm
    inner_width = models.FloatField(validators=[MinValueValidator(0.01)])   # cm
    inner_height = models.FloatField(validators=[MinValueValidator(0.01)])  # cm
    max_weight = models.FloatField(validators=[MinValueValidator(0.01)])    # kg
    cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def inner_volume(self):
        return self.inner_length * self.inner_width * self.inner_height


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderItem")
    recommended_box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order.pk})"
