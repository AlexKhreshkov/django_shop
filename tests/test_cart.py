from django.contrib.auth.models import User
from django.test import TestCase
from app.cart import Cart
from django.test.client import RequestFactory
from app.models import Item, Category


class TestCart(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='laptop', slug='laptop')
        category = Category.objects.get(name='laptop')
        Item.objects.create(
            title='MSI GF63 15.6" 144 H',
            price=1234.99,
            category=category,
            slug='msi-gf63-156-144-h',
            description='Some text',
            image='test_image.png',
            mark=4.99,
        )

    def test_cart_init(self):
        self.client.get('')
        cart = Cart(self.client)
        self.assertEquals(cart.session['cart'], {})

    def test_add_to_cart(self):
        self.client.get('')
        cart = Cart(self.client)
        item = Item.objects.get(id=1)
        cart.add_product(item)
        self.assertEquals(cart.session['cart']['1'], {'quantity': '1',
                                                      'price': '1234.99'})

    def test_remove_from_cart(self):
        self.client.get('')
        cart = Cart(self.client)
        item = Item.objects.get(id=1)
        cart.add_product(item)
        cart.remove(item)
        self.assertEquals(cart.session['cart'], {})

    def test_clear_cart(self):
        self.client.get('')
        cart = Cart(self.client)
        item = Item.objects.get(id=1)
        cart.add_product(item)
        cart.clear()
        self.assertEquals(cart.session.get('cart'), None)

    def test_check_cart_len(self):
        self.client.get('')
        cart = Cart(self.client)
        item = Item.objects.get(id=1)
        cart.add_product(item)
        cart_len = cart.cart_len()
        self.assertEquals(cart_len, 1)

    def test_cart_total_price(self):
        self.client.get('')
        cart = Cart(self.client)
        item = Item.objects.get(id=1)
        cart.add_product(item)
        total_price = cart.get_total_price()
        self.assertEquals(total_price, 1234.99)

    def test_change_cart_quantity(self):
        self.client.get('')
        cart = Cart(self.client)
        item = Item.objects.get(id=1)
        cart.add_product(item)
        cart.change_quantity(item, 5)
        new_total_price = cart.get_total_price()
        self.assertEquals(new_total_price, 5 * 1234.99)
