from statistics import mean

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.decorators.http import require_POST

from app.forms import UpdateCountForm, OrderForm, AddCommentForm, UserProfileForm, AddUserInfoForm, \
    AddProfileInfoForm
from app.models import Item, Category, Cart, User, Profile, Order, RatingMark, Comment


def main(request):
    items = Item.objects.all()
    categories = Category.objects.all()
    cart = Cart(request)
    cart_len = cart.cart_len()
    context = {
        'items': items,
        'categories': categories,
        'title': 'Main page',
        'category': 'all',
        'cart': cart,
        'cart_len': cart_len,
        'page_name': 'main',
    }
    return render(request, 'app/main.html', context=context)


def show_by_category(request, cat_slug):
    categories = Category.objects.all()
    chosen_category = Category.objects.get(slug=cat_slug)
    items = Item.objects.filter(category=chosen_category)
    title = chosen_category.name
    cart = Cart(request)
    cart_len = cart.cart_len()
    context = {
        'items': items,
        'categories': categories,
        'title': title,
        'cart': cart,
        'cart_len': cart_len,
    }
    return render(request, 'app/main.html', context=context)


def show_item(request, item_slug):
    """adding comments from admin doesn't change rating"""

    item = Item.objects.get(slug=item_slug)
    title = item.title
    comments = Comment.objects.filter(item_id__slug=item_slug)
    form = AddCommentForm()
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.item = item
            form.save()
            # initially item.mark is None, comments = 0. Then we create first comment => comments.count = 1
            if comments.count() == 1:
                item.mark = form.mark.mark
                item.save()
            else:
                sum_of_all_marks = 0
                comments_count = comments.count()
                for comment in comments:
                    sum_of_all_marks += comment.mark.mark
                    avg_mark = round(sum_of_all_marks / comments_count, 1)
                    print(sum_of_all_marks, comments_count, avg_mark)
                item.mark = avg_mark
                item.save()
            return redirect(item.get_absolute_url())
    context = {
        'item': item,
        'title': title,
        'comments': comments,
        'form': form,
    }
    return render(request, 'app/item.html', context=context)


def delete_comment(request, item_slug, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    item = get_object_or_404(Item, slug=item_slug)
    if comment.user == request.user or request.user.is_superuser:
        comments = Comment.objects.filter(item_id__slug=item_slug)
        com_count = comments.count()
        item_mark = item.mark
        com_mark = comment.mark.mark
        if comments.count() == 1:
            item.mark = None
        else:
            item.mark = round((comments.count() * item.mark - comment.mark.mark) / (comments.count() - 1), 1)
        item.save()
        comment.delete()
        return redirect(item.get_absolute_url())
    else:
        return redirect(item.get_absolute_url())


def add_to_cart(request, item_slug):
    c = Cart(request)
    item = get_object_or_404(Item, slug=item_slug)
    c.add_product(item)
    return redirect('show_cart')


def remove_from_cart(request, item_slug):
    c = Cart(request)
    item = get_object_or_404(Item, slug=item_slug)
    c.remove(item)
    return redirect('show_cart')


def show_cart(request):
    cart = Cart(request)
    is_cart = bool(cart)
    form = UpdateCountForm
    return render(request, 'app/cart.html', {'cart': cart, 'form': form, 'title': 'Cart'})


def update_count(request, item_slug):
    cart = Cart(request)
    form = UpdateCountForm(request.POST)
    print(request.POST)
    if form.is_valid():
        item = get_object_or_404(Item, slug=item_slug)
        cart.change_quantity(item, form.cleaned_data['quantity'])
    return redirect('show_cart')


def show_profile(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    user = get_object_or_404(User, id=pk)
    if request.user == user or request.user.is_superuser:
        orders = Order.objects.filter(user_id=pk)
        user_form = UserProfileForm()
        if request.method == 'POST':
            profile_form = AddProfileInfoForm(request.POST, request.FILES, instance=profile)
            print(request.POST)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('user_profile', pk)
            else:
                print(profile_form.errors.as_data())  # here you print errors to terminal
        else:
            profile_form = AddProfileInfoForm(
                {
                    'phone': user.profile.phone,
                    'birth_date': user.profile.birth_date,
                    'location': user.profile.location
                })
        context = {
            'user_profile': profile,
            'orders': orders,
            'user': user,
            'title': f"{user.username}'s profile",
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(request, 'app/profile.html', context=context)
    else:
        raise Http404("Access forbidden. You can't see another user's profile")


def make_order(request):
    cart = Cart(request)
    is_cart = bool(cart)
    order_items = [item for item in Item.objects.filter(id__in=cart.cart.keys())]
    if request.method == 'POST':
        updated_request = request.POST.copy()
        items_id_list = Item.objects.filter(id__in=cart.cart.keys())
        updated_request.update({
            'total_cost': cart.get_total_price(),
            'user': request.user.id,
        })
        form = OrderForm(updated_request)
        print(updated_request)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('user_profile', request.user.id)
        else:
            print(form.errors)

    else:
        form = OrderForm()
    context = {
        'cart': cart,
        'form': form,
        'title': 'Order',
        'order_items': order_items,
    }
    return render(request, 'app/order.html', context=context)
