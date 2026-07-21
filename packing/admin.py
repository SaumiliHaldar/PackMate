from django.contrib import admin
from .models import Box, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'length', 'width', 'height', 'weight']
    search_fields = ['name']


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inner_length', 'inner_width', 'inner_height',
                    'max_weight', 'cost']
    ordering = ['cost']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    inlines = [OrderItemInline]
    ordering = ['-created_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
