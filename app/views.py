from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from app.cart import Cart
from app.forms import *
from app.models import Item, Category, Profile, Order, Comment, RatingMark
from app.utils import GetMainPageContextDataMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPageView(GetMainPageContextDataMixin, ListView):
    template_name = 'app/main.html'
    context_object_name = 'items'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_context_data_mixin(title='Online shop')
        return context | mixin_context

    def get_queryset(self):
        return Item.objects.all().select_related('category').order_by('-mark')


class Search(GetMainPageContextDataMixin, ListView):
    template_name = 'app/main.html'
    context_object_name = 'items'

    def search_check(self):
        search_text = self.request.GET.get('text')
        items = Item.objects.all()
        suitable_items = [item for item in items if search_text in item.title or search_text in item.description]
        items = Item.objects.filter(title__in=suitable_items).select_related('category')
        return items

    def get_queryset(self):
        return self.search_check()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_context_data_mixin(title='Online shop')
        context['text'] = self.request.GET.get('text')
        context['is_founded_items'] = self.search_check().count()
        return context | mixin_context


class ShowCategoryView(ListView):
    template_name = 'app/main.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.select_related('category').filter(category__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['chosen_category'] = Category.objects.get(slug=self.kwargs['cat_slug'])
        context['title'] = context['chosen_category'].name
        cart = Cart(self.request)
        context['cart'] = cart
        context['cart_len'] = cart.cart_len()
        return context


class ItemDetail(DetailView):
    model = Item
    slug_url_kwarg = 'item_slug'
    template_name = 'app/item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(item_id__slug=self.kwargs['item_slug']). \
            select_related('item', 'mark', 'user', 'user__profile')
        context['form'] = AddCommentForm()
        context['title'] = self.kwargs['item_slug']
        return context


def recalculate_item_rating(item_slug):
    item = Item.objects.get(slug=item_slug)
    comments_sum = 0
    for comment in Comment.objects.filter(item=item):
        comments_sum += comment.mark.mark
    avg_mark = comments_sum / Comment.objects.filter(item=item).count()
    return avg_mark


class AddComment(View):
    def post(self, request, item_slug):
        form = AddCommentForm(request.POST)
        item = Item.objects.get(slug=item_slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.item = item
            form.user = self.request.user
            form.save()

        return redirect(item.get_absolute_url())


class DeleteComment(View):
    def get(self, request, item_slug, comment_id):
        item = Item.objects.get(slug=item_slug)
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        item.mark = recalculate_item_rating(item_slug)
        item.save()
        return redirect(item.get_absolute_url())


class ShowChangeableComment(View):
    def get(self, request, item_slug, comment_id):
        changeable_comment = get_object_or_404(Comment, pk=comment_id)
        item = get_object_or_404(Item, slug=item_slug)
        comments = Comment.objects.filter(item_id__slug=item_slug). \
            select_related('item', 'mark', 'user', 'user__profile')
        form = ChangeCommentForm(instance=changeable_comment)
        context = {
            'item': item,
            'title': item.title,
            'comments': comments,
            'form': form,
            'changeable_comment': changeable_comment,
        }
        return render(request, 'app/change_comment.html', context=context)

    def post(self, request, item_slug, comment_id):
        changeable_comment = get_object_or_404(Comment, pk=comment_id)
        item = get_object_or_404(Item, slug=item_slug)
        changeable_comment.mark = RatingMark.objects.get(mark=request.POST.get('mark'))
        changeable_comment.text = request.POST.get('text')
        changeable_comment.save()
        item.mark = recalculate_item_rating(item_slug)
        item.save()
        return redirect(item.get_absolute_url())


class AddToCart(View):
    def post(self, request, item_slug):
        c = Cart(request)
        item = get_object_or_404(Item, slug=item_slug)
        c.add_product(item)
        return redirect('show_cart')


class RemoveFromCart(View):
    def post(self, request, item_slug):
        c = Cart(request)
        item = get_object_or_404(Item, slug=item_slug)
        c.remove(item)
        return redirect('show_cart')


class ShowCart(View):
    def get(self, request):
        cart = Cart(request)
        form = UpdateCountForm
        return render(request, 'app/cart.html', {'cart': cart, 'form': form, 'title': 'Cart'})


class UpdateCartCount(View):
    def post(self, request, item_slug):
        cart = Cart(request)
        form = UpdateCountForm(request.POST)
        if form.is_valid():
            item = get_object_or_404(Item, slug=item_slug)
            cart.change_quantity(item, form.cleaned_data['quantity'])
        return redirect('show_cart')


class ShowProfile(LoginRequiredMixin, View):
    def get(self, request, pk):
        user_profile = get_object_or_404(Profile, user_id=pk)
        if request.user == self.request.user or request.user.is_superuser:
            orders = Order.objects.filter(user_id=pk).select_related('user').prefetch_related('items')
            context = {
                'user_profile': user_profile,
                'orders': orders,
                'username': f"{self.request.user.username}'s profile",
                'profile_form': AddProfileInfoForm({
                    'phone': user_profile.phone,
                    'birth_date': user_profile.birth_date,
                    'location': user_profile.location,
                }),
                'title': f"{self.request.user.username}'s profile",
            }
        else:
            raise Http404("Access forbidden. You can't see another user's profile")
        return render(request, 'app/profile.html', context=context)


class UpdateProfile(UpdateView):
    model = Profile
    form_class = AddProfileInfoForm

    def get_success_url(self):
        return reverse('user_profile', kwargs={'pk': self.kwargs.get('pk')})


class MakeOrder(View):
    def get(self, request):
        cart = Cart(request)
        order_items = [item for item in Item.objects.filter(id__in=cart.cart.keys())]
        current_user = self.request.user
        form = OrderForm({'full_name': current_user.profile.user, 'phone': current_user.profile.phone})
        context = {
            'cart': cart,
            'form': form,
            'title': 'Order',
            'order_items': order_items,
        }
        return render(request, 'app/order.html', context=context)

    def post(self, request):
        form = OrderForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.total_cost = cart.get_total_price()
            items = Item.objects.filter(id__in=cart.cart.keys())
            items_id = [i.id for i in items]
            form.save()
            form.items.add(*items_id)
            form.save()
        return redirect('user_profile', request.user.id)
