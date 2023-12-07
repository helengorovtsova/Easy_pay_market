from django.contrib import admin

from .models import Discount, Item, Order, Tax  

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description')
    search_fields = ('name', 'price')
    list_filter = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'items_price', 'total_price')


admin.site.register(Discount)

admin.site.register(Tax)
