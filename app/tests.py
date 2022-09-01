from django.test import TestCase
from app.models import *


class TestMainPage(TestCase):

    def setUp(self) -> None:
        category = Category.objects.create(name='laptops', slug='laptops')
        item = Item.objects.create(
            title='Lenovo pro book 123',
            price=999,
            slug='lenovo-pro-book-123',
            description='Lenovo pro book 123 is a good laptop',
            category=category,
        )

    def test_main_page_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
