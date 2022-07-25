from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from app.models import Category, Item, Profile, Order, RatingMark, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'get_item_image')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

    def get_item_image(self, item_obj):
        if item_obj:
            return mark_safe(f"<img src='{item_obj.image.url}' width=50>")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'location', 'birth_date', 'phone')


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'get_order_name', 'user_id', 'status', 'get_item_image', 'show_items', 'created', 'updated', 'delivery_address',
        'issue_point',
        'phone', 'show_cost')

    def get_order_name(self, obj):
        return f"Order№{obj.id}"

    def get_item_image(self, obj):
        return mark_safe([f"<img src='{item.image.url}' width=50>" for item in obj.items.all() if item.image.url])

    def show_cost(self, obj):
        return obj.total_cost

    def show_items(self, obj):
        return [f"Name: {item.title}, Price: {item.price}" for item in obj.items.all()]


class RatingMarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'mark')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created', 'item', 'mark', 'user')
    list_display_links = ('id', 'text', 'item', 'mark', 'user')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(RatingMark, RatingMarkAdmin)
admin.site.register(Comment, CommentAdmin)
