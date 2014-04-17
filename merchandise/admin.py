from django.contrib import admin
from merchandise.models import Bundle, Item, BundleOrder, ItemOrder


class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('item', 'school', 'bundle_order', 'quantity', 'total_cost',
                    'total_owed_by_school', 'is_finalised')
    ordering = ['school']


class ItemOrderInline(admin.StackedInline):
    model = ItemOrder


class BundleOrderAdmin(admin.ModelAdmin):
    inlines = [ItemOrderInline]
    list_display = ('bundle', 'school', 'quantity', 'comment')


admin.site.register(Bundle)
admin.site.register(Item)
admin.site.register(BundleOrder, BundleOrderAdmin)
admin.site.register(ItemOrder, ItemOrderAdmin)
