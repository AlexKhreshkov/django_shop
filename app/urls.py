from django.urls import path, include

from app.views import main, show_by_category, show_item, show_cart, add_to_cart, remove_from_cart, update_count, \
    show_profile, make_order

urlpatterns = [
    path('', main, name='main'),
    path('category/<slug:cat_slug>/', show_by_category, name='show_by_category'),
    path('product/<slug:item_slug>/', show_item, name='show_item'),
    path('add/<slug:item_slug>/', add_to_cart, name='add_item'),
    path('cart/', show_cart, name='show_cart'),
    path('remove/<slug:item_slug>/', remove_from_cart, name='delete_item'),
    path('cart/update-item-count/<slug:item_slug>/', update_count, name='update_count'),
    path('user-profile/<int:pk>/', show_profile, name='user_profile'),
    path('order/', make_order, name='make_order'),
]
