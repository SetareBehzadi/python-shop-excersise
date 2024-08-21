from django.db import models
from   django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subCategory')
    is_sub = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} -> {self.slug}'

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    category = models.ManyToManyField(Category, related_name='products')
    price = models.BigIntegerField()
    image = models.ImageField()
    description = models.TextField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('home:product-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name}'