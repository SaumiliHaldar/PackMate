"""
Unit tests for selector.py — pure logic, no database.
"""
from django.test import TestCase
from packing.selector import find_best_box


def make_item(l, w, h, weight, qty=1):
    return {
        'length': l, 'width': w, 'height': h,
        'weight': weight,
        'volume': l * w * h,
        'quantity': qty,
    }


def make_box(id, name, il, iw, ih, max_weight, cost):
    return {
        'id': id, 'name': name,
        'inner_length': il, 'inner_width': iw, 'inner_height': ih,
        'max_weight': max_weight,
        'inner_volume': il * iw * ih,
        'cost': cost,
    }


SMALL  = make_box(1, 'Small',  20, 20, 20, max_weight=5,  cost=2.00)
MEDIUM = make_box(2, 'Medium', 40, 40, 40, max_weight=15, cost=5.00)
LARGE  = make_box(3, 'Large',  60, 60, 60, max_weight=30, cost=9.00)
ALL_BOXES = [SMALL, MEDIUM, LARGE]


class SelectorFitTests(TestCase):

    def test_single_item_fits_smallest_box(self):
        items = [make_item(10, 10, 10, weight=1)]
        result = find_best_box(items, ALL_BOXES)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Small')

    def test_picks_cheapest_valid_box(self):
        # Fits Medium and Large — should pick Medium (cheaper)
        items = [make_item(30, 30, 30, weight=10)]
        result = find_best_box(items, ALL_BOXES)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Medium')

    def test_heavy_order_skips_small_box(self):
        # Weight 12 kg — exceeds Small (5 kg) and Medium (15 kg - ok), pick Medium
        items = [make_item(10, 10, 10, weight=12)]
        result = find_best_box(items, ALL_BOXES)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Medium')

    def test_multiple_items_picks_correct_box(self):
        # Two items, combined weight 8 kg — Small (max 5 kg) excluded, Medium fits
        items = [make_item(10, 10, 10, weight=4, qty=2)]
        result = find_best_box(items, ALL_BOXES)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Medium')

    def test_item_too_large_returns_none(self):
        # Item 70cm on one side — bigger than all boxes
        items = [make_item(70, 10, 10, weight=1)]
        result = find_best_box(items, ALL_BOXES)
        self.assertIsNone(result)

    def test_total_weight_exceeds_all_boxes_returns_none(self):
        items = [make_item(10, 10, 10, weight=50)]
        result = find_best_box(items, ALL_BOXES)
        self.assertIsNone(result)

    def test_volume_overflow_returns_none(self):
        # Many tiny items whose total volume exceeds all boxes
        items = [make_item(5, 5, 5, weight=0.1, qty=500)]
        result = find_best_box(items, ALL_BOXES)
        self.assertIsNone(result)

    def test_long_thin_item_fails_dimension_check(self):
        # A 50cm long item — fits in Large (60cm) but NOT Small or Medium (40cm)
        items = [make_item(50, 5, 5, weight=1)]
        result = find_best_box(items, ALL_BOXES)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Large')

    def test_empty_order_returns_none(self):
        result = find_best_box([], ALL_BOXES)
        self.assertIsNone(result)

    def test_no_boxes_returns_none(self):
        items = [make_item(10, 10, 10, weight=1)]
        result = find_best_box(items, [])
        self.assertIsNone(result)
