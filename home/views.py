from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Category
from . import tasks
from django.contrib import messages
from utils import UserIsAdmin

from orders.forms import CartAddForm


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)

        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, 'home/detail.html', {'product': product, 'form': form})


class BucketView(UserIsAdmin, View):
    template_name = 'home/bucket.html'

    def get(self, request):
        # res = all_buckets_objects_task.delay()
        res = tasks.all_buckets_objects_task()
        print('=' * 20)
        print(res)

        return render(request, self.template_name, {'objects': res})


class BucketDeleteObjectView(UserIsAdmin, View):
    def get(self, request, key):
        tasks.delete_object_ask.delay(key)
        messages.success(request, 'Your image delete successfully', 'info')
        return redirect('home:bucket')


class BucketDownloadObjectView(UserIsAdmin, View):

    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'Your image Download successfully', 'info')
        return redirect('home:bucket')
