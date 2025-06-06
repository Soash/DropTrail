from django.contrib import admin
from .models import Product, Category, Image, Banner, Order

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
        
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('name', 'category', 'price')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'category')
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'cateImage', 'slug')
        }),
    )

class ImageAdmin(admin.ModelAdmin):
    search_fields = ['product__name']
    list_display = ('product_name', 'image')

    def product_name(self, obj):
        return obj.product.name
    
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'banner')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Order, OrderAdmin)


