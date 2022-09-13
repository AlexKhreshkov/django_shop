from .cart import Cart
from .forms import SearchForm
from .models import *


class GetMainPageContextDataMixin():
    def get_context_data_mixin(self, **kwargs):
        context = kwargs
        context['page_name'] = 'main'
        context['category'] = 'all'
        context['categories'] = Category.objects.all().values('name','slug')
        cart = Cart(self.request)
        context['cart'] = cart
        context['cart_len'] = cart.cart_len()
        context['form'] = SearchForm()
        return context
