from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class StockMovement(models.Model):
    MOVEMENT_CHOICES = [
        ('IN', 'Hyrje'),
        ('OUT', 'DALJE'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_movements') 
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} - {self.product} - ({self.quantity})"
    