from app.models import Item


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def __str__(self):
        return f"session: {self.session}, cart:{self.cart}"

    def save(self):
        self.session.modified = True

    def add_product(self, product):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart[product_id] = {
                'quantity': '1',
                'price': str(product.price)
            }
        else:
            print('Product already in the cart')
        self.save()

    def cart_len(self):
        return len(self.cart)

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Item.objects.filter(id__in=product_ids)  # 1 2 3
        # cart:{'1': {'quantity': '1', 'price': '999.0'}}`
        for product in products:
            product.quantity = int(self.cart[str(product.id)]['quantity'])
            product.price = float(self.cart[str(product.id)]['price'])
            product.total_price = product.quantity * product.price
            yield product

    def get_total_price(self):
        return sum(float(item['price']) * int(item['quantity']) for item in self.cart.values())

    def remove(self, product):
        if str(product.id) in self.cart.keys():
            del self.cart[str(product.id)]
            self.save()

    def change_quantity(self, product, quantity):
        self.cart[str(product.id)]['quantity'] = quantity
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()
