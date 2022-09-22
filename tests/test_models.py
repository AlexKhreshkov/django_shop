from django.test import TestCase
from app.models import *
from app.constants import MAX_RATING_MARK, MIN_RATING_MARK, ALLOWED_ORDER_STATUSES


class TestCategoryModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='laptop', slug='laptop')

    def test_category_name_max_length(self):
        category = Category.objects.get(name='laptop')
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_slug_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('slug').max_length
        self.assertEquals(max_length, 50)

    def test_category_absolute_url(self):
        category = Category.objects.get(id=1)
        self.assertEquals(category.get_absolute_url(), f'/category/{category.slug}/')


class TestItemModel(TestCase):

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

    def test_item_mark_range(self):
        item = Item.objects.get(id=1)
        self.assertTrue(MIN_RATING_MARK <= item.mark <= MAX_RATING_MARK)

    def test_item_absolute_url(self):
        item = Item.objects.get(id=1)
        self.assertEquals(item.get_absolute_url(), f'/product/{item.slug}/')


class TestRatingMarkModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        RatingMark.objects.create(mark=3)

    def test_rating_mark_range(self):
        rating_mark = RatingMark.objects.get(id=1)
        self.assertIn(rating_mark.mark, range(MIN_RATING_MARK, MAX_RATING_MARK + 1))


class TestOrderModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='just_user')
        Order.objects.create(
            status='done',
            created='2022-06-14',
            updated='2022-06-14',
            full_name='alex alex',
            phone='+64123123',
            total_cost=1234,
            delivery_address='My address',
            user=User.objects.get(username='just_user')
        )

    def test_status(self):
        order = Order.objects.get(id=1)
        self.assertIn(order.status, ALLOWED_ORDER_STATUSES)
