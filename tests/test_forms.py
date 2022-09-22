import random
from app.forms import *
from django.test import TestCase
from app.constants import MIN_ITEMS_COUNT_CART, MAX_ITEMS_COUNT_CART, ALLOWED_ORDER_ISSUES_POINTS, MIN_RATING_MARK, \
    MAX_RATING_MARK
from app.models import RatingMark


class TestUpdateCountForm(TestCase):

    def setUp(self):
        self.allowed_quantity = random.randint(MIN_ITEMS_COUNT_CART, MAX_ITEMS_COUNT_CART)
        self.less_than_allowed_quantity = self.allowed_quantity ** -1
        self.more_than_allowed_quantity = self.allowed_quantity + 1000

    def test_valid_quantity(self):
        form_data = {'quantity': self.allowed_quantity}
        form = UpdateCountForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_less_quantity(self):
        form_data = {'quantity': self.less_than_allowed_quantity}
        form = UpdateCountForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_more_quantity(self):
        form_data = {'quantity': self.more_than_allowed_quantity}
        form = UpdateCountForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestOrderForm(TestCase):

    def test_order_without_issue_point(self):
        form_data = {
            'full_name': 'alex alex',
            'phone': '+1231233',
            'delivery_address': 'str. asd 123'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_without_delivery_address(self):
        form_data = {
            'full_name': 'alex alex',
            'phone': '+1231233',
            'issue_point': ALLOWED_ORDER_ISSUES_POINTS[0]
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_without_delivery_issue_point(self):
        form_data = {
            'full_name': 'alex alex',
            'phone': '+1231233',
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestAddCommentForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        RatingMark.objects.create(mark=1)

    def test_comment_valid_mark(self):
        rating_mark = RatingMark.objects.get(pk=1)
        form_data = {
            'text': 'Hello!',
            'mark': rating_mark,
        }
        form = AddCommentForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestChangeCommentForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        RatingMark.objects.create(mark=1)

    def test_comment_valid_mark(self):
        rating_mark = RatingMark.objects.get(pk=1).id
        form_data = {
            'text': 'New text',
            'mark': rating_mark,
            # 'mark': 1
        }
        form = AddCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_invalid_mark(self):
        form_data = {
            'text': 'New text',
            'mark': 7,
        }
        form = AddCommentForm(data=form_data)
        self.assertFalse(form.is_valid())
