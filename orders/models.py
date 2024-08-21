from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator,MinValueValidator

from home.models import Product


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('paid', '-updated_at')

    def __str__(self):
        return f'{self.user} - str({self.id}) '

    def get_total_order_price(self):
        total =  sum(item.get_total_price() for item in self.items.all())
        if self.discount:
            discount = (self.discount/100) * total
            return int(total - discount)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{str(self.id) }'

    def get_total_price(self):
        return self.price * self.quantity


class Coupon(models.Model):
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(90)])
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self):
        return self.code

