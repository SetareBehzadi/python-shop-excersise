from django.urls import path, include

from home.views import HomeView, ProductDetailView, BucketView, BucketDeleteObjectView, BucketDownloadObjectView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'
bucket_urls = [
    path('', BucketView.as_view(), name='bucket'),
    path('delete_obj/<str:key>/', BucketDeleteObjectView .as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>/', BucketDownloadObjectView .as_view(), name='download_obj_bucket'),

]


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('bucket/', include(bucket_urls)),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:category_slug>/', HomeView.as_view(), name='category_filter'),
]