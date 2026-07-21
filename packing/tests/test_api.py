"""
API integration tests — hits the actual endpoints via Django test client.
"""
import json
from django.test import TestCase
from django.urls import reverse
from packing.models import Box, Order, Product


class ProductAPITests(TestCase):

    def test_create_product(self):
        res = self.client.post('/products/', {
            'name': 'Widget', 'length': 10, 'width': 5, 'height': 3, 'weight': 0.5
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['name'], 'Widget')

    def test_create_product_zero_dimension_rejected(self):
        res = self.client.post('/products/', {
            'name': 'Bad', 'length': 0, 'width': 5, 'height': 3, 'weight': 0.5
        }, content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_create_product_negative_weight_rejected(self):
        res = self.client.post('/products/', {
            'name': 'Bad', 'length': 10, 'width': 5, 'height': 3, 'weight': -1
        }, content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_list_products(self):
        Product.objects.create(name='P1', length=10, width=10, height=10, weight=1)
        res = self.client.get('/products/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)


class BoxAPITests(TestCase):

    def test_create_box(self):
        res = self.client.post('/boxes/', {
            'name': 'Small', 'inner_length': 20, 'inner_width': 20,
            'inner_height': 20, 'max_weight': 5, 'cost': '2.00'
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_create_box_zero_dimension_rejected(self):
        res = self.client.post('/boxes/', {
            'name': 'Bad', 'inner_length': 0, 'inner_width': 20,
            'inner_height': 20, 'max_weight': 5, 'cost': '2.00'
        }, content_type='application/json')
        self.assertEqual(res.status_code, 400)


class OrderAPITests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Widget', length=10, width=10, height=10, weight=1
        )
        self.box = Box.objects.create(
            name='Small', inner_length=20, inner_width=20, inner_height=20,
            max_weight=5, cost=2.00
        )

    def test_create_order(self):
        res = self.client.post('/orders/', {
            'items': [{'product_id': self.product.id, 'quantity': 1}]
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(res.data['items']), 1)

    def test_create_order_empty_items_rejected(self):
        res = self.client.post('/orders/', {'items': []},
                               content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_create_order_zero_quantity_rejected(self):
        res = self.client.post('/orders/', {
            'items': [{'product_id': self.product.id, 'quantity': 0}]
        }, content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_create_order_invalid_product_rejected(self):
        res = self.client.post('/orders/', {
            'items': [{'product_id': 9999, 'quantity': 1}]
        }, content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_create_order_duplicate_products_rejected(self):
        res = self.client.post('/orders/', {
            'items': [
                {'product_id': self.product.id, 'quantity': 1},
                {'product_id': self.product.id, 'quantity': 2},
            ]
        }, content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_list_orders(self):
        order = Order.objects.create()
        res = self.client.get('/orders/')
        self.assertEqual(res.status_code, 200)


class RecommendAPITests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Widget', length=10, width=10, height=10, weight=1
        )
        self.box_small = Box.objects.create(
            name='Small', inner_length=20, inner_width=20, inner_height=20,
            max_weight=5, cost=2.00
        )
        self.box_large = Box.objects.create(
            name='Large', inner_length=60, inner_width=60, inner_height=60,
            max_weight=30, cost=9.00
        )

    def _create_order(self, product, qty=1):
        res = self.client.post('/orders/', {
            'items': [{'product_id': product.id, 'quantity': qty}]
        }, content_type='application/json')
        return res.data['id']

    def test_recommend_returns_cheapest_valid_box(self):
        order_id = self._create_order(self.product, qty=1)
        res = self.client.get(f'/orders/{order_id}/recommend/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['name'], 'Small')

    def test_recommend_404_when_no_box_fits(self):
        # Product too heavy for any box
        heavy = Product.objects.create(
            name='Anvil', length=5, width=5, height=5, weight=100
        )
        order_id = self._create_order(heavy, qty=1)
        res = self.client.get(f'/orders/{order_id}/recommend/')
        self.assertEqual(res.status_code, 404)
        self.assertIn('No suitable box found', res.data['detail'])

    def test_recommend_404_for_nonexistent_order(self):
        res = self.client.get('/orders/9999/recommend/')
        self.assertEqual(res.status_code, 404)
