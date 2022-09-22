from django.test import TestCase
from app.models import *
from app.constants import MAX_RATING_MARK, MIN_RATING_MARK, ALLOWED_ORDER_STATUSES


class TestMainPageView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create 21 item for tests
        Category.objects.create(name='laptop', slug='laptop')
        laptop_category = Category.objects.get(name='laptop')
        items_count = 21
        for i in range(items_count):
            Item.objects.create(
                title=f'testitem{i}',
                price=1234.99,
                category=laptop_category,
                slug=f'testitem{i}',
                description='Some text',
                image='test_image.png',
                mark=4.99,
            )

    def test_view_url_exist(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app/main.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['items']) == 3)

    def test_list_all_items(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('main') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['items']) == 3)


class TestShowCategoryView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create 21 item for tests
        Category.objects.create(name='laptop', slug='laptop')
        laptop_category = Category.objects.get(name='laptop')
        Item.objects.create(
            title='testitem',
            price=1234.99,
            category=laptop_category,
            slug='testitem',
            description='Some text',
            image='test_image.png',
            mark=4.99,
        )
        cls.item = Item.objects.get(slug='testitem')

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse(('show_item'), kwargs={'item_slug': self.item.slug}))
        self.assertEqual(resp.status_code, 200)
