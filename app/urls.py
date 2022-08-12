from django.urls import path, include

from app.views import *

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
    path('product/<slug:item_slug>/comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('product/<slug:item_slug>/comment/change/<int:comment_id>/', change_comment, name='change_comment'),
]
