from django.urls import path
from app.views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('search/', Search.as_view(), name='search'),
    path('category/<slug:cat_slug>/', ShowCategoryView.as_view(), name='show_by_category'),
    path('product/<slug:item_slug>/', ItemDetail.as_view(), name='show_item'),
    path('add/<slug:item_slug>/', AddToCart.as_view(), name='add_item'),
    path('cart/', ShowCart.as_view(), name='show_cart'),
    path('remove/<slug:item_slug>/', RemoveFromCart.as_view(), name='delete_item'),
    path('cart/update-item-count/<slug:item_slug>/', UpdateCartCount.as_view(), name='update_count'),
    path('user-profile/<int:pk>/', ShowProfile.as_view(), name='user_profile'),
    path('user-profile/update/<int:pk>/', UpdateProfile.as_view(), name='update_profile'),
    path('order/', MakeOrder.as_view(), name='make_order'),
    path('add_comment/<slug:item_slug>/', AddComment.as_view(), name='add_comment'),
    path('product/<slug:item_slug>/comment/delete/<int:comment_id>/', DeleteComment.as_view(), name='delete_comment'),
    path('product/<slug:item_slug>/comment/change/<int:comment_id>/', ShowChangeableComment.as_view(),
         name='show_changeable_comment'),
]
