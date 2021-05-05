from django.contrib import admin

from ecommerce.models import Category, Product, ProductHasImage, ProductReview, WishList, Cart


class ProductHasImageInline(admin.TabularInline):
    model = ProductHasImage


class AdminProduct(admin.ModelAdmin):
    inlines = [ProductHasImageInline]


admin.site.register(Category)

admin.site.register(Product, AdminProduct)  # product sangai image pani upload garna milxa admin panal ma
# it merges Product and ProductHasImage in. ProductHas image is child of parent Product.Check django admin tabular inline
#The admin interface has the ability to edit models on the same page as a parent model. These are called inlines

admin.site.register(ProductReview)
admin.site.register(ProductHasImage)

admin.site.register(WishList)

admin.site.register(Cart)
