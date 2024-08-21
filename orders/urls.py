from django.urls import path

from orders.views import CartView, CartAddView, CartRemoveView, CreateOderView, OrderDetailView, OrderPayView, \
    OrderVerifyView, CouponApplyView

app_name = 'order'
urlpatterns = [
    path('create/', CreateOderView.as_view(), name='order_create'),
    path('detail/<int:order_id>', OrderDetailView.as_view(), name='order_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>', CartAddView.as_view(), name='cart'),
    path('cart/remove/<int:product_id>', CartRemoveView.as_view(), name='remove'),
    path('pay/<int:order_id>/', OrderPayView.as_view(), name='order_pay'),
    path('verify/', OrderVerifyView.as_view(), name='order_verify'),
    path('apply/<int:order_id>/', CouponApplyView.as_view(), name='apply_coupon'),
]
