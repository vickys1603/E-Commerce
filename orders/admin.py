from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product'] # Useful for many products
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'email', 'get_total_cost', 'created_at', 'paid')
    list_filter = ('paid', 'created_at')
    search_fields = ('id', 'first_name', 'last_name', 'email')
    inlines = [OrderItemInline]

    def get_total_cost(self, obj):
        return obj.get_total_cost()
    get_total_cost.short_description = 'Total Cost'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity', 'get_cost')
    list_filter = ('order__created_at',)
    search_fields = ('product__name', 'order__id')

    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'Cost'