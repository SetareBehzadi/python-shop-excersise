from django.contrib import admin

from orders.models import OrderItem, Order, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated_at', 'paid')
    list_filter = ('paid',)
    inlines = (OrderItemInline,)

@admin.register(Coupon)
class CouponOrder(admin.ModelAdmin):
    list_display = ('code', 'discount')
    list_filter = ('active',)
