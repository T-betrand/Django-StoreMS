from django.contrib import admin

from .models import Stock , Category
from .forms import StockCreateForm


class StockCreationAdmin(admin.ModelAdmin):
    list_display = ['category', 'item_name', 'timestamp', 'last_updated', 'quantity']
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']


# Register your models here.
# admin.site.register(Stock)
admin.site.register(Stock, StockCreationAdmin)
admin.site.register(Category)
