"""
Management command: python manage.py seed_data

Seeds the database with sample products and boxes.
Safe to run multiple times — skips already-existing records by name.
"""
from django.core.management.base import BaseCommand
from packing.models import Box, Product


PRODUCTS = [
    # name,              L,    W,   H,   weight
    ("Laptop",           35,   25,  3,   2.10),
    ("Smartphone",       16,    8,  1,   0.20),
    ("Hardcover Book",   24,   17,  4,   0.55),
    ("Ceramic Mug",      12,   12, 10,   0.40),
    ("Wireless Headphones", 20, 18,  8,  0.35),
    ("Tablet",           25,   17,  1,   0.65),
    ("DSLR Camera Body", 14,   10,  8,   0.85),
    ("Gaming Controller",18,   12,  7,   0.30),
    ("Running Shoes",    32,   20, 13,   0.90),
    ("Water Bottle",      8,    8, 28,   0.25),
    ("Smart Watch",      12,    6,  5,   0.10),
    ("Bluetooth Speaker",20,   14, 10,   0.60),
]

BOXES = [
    # name,         inner_L, inner_W, inner_H, max_weight, cost
    ("Tiny Box",        16,    12,    10,   1.0,   15.00),
    ("Small Box",       28,    22,    16,   3.0,   28.00),
    ("Medium Box",      38,    32,    26,   8.0,   48.00),
    ("Large Box",       52,    42,    36,  15.0,   75.00),
    ("XL Box",          66,    56,    46,  25.0,  110.00),
    ("Heavy Duty Box",  42,    36,    32,  35.0,   92.00),
]


class Command(BaseCommand):
    help = "Seeds the database with sample products and boxes."

    def handle(self, *args, **options):
        created_p = 0
        for name, l, w, h, weight in PRODUCTS:
            _, created = Product.objects.get_or_create(
                name=name,
                defaults=dict(length=l, width=w, height=h, weight=weight),
            )
            if created:
                created_p += 1
                self.stdout.write(f"  + Product: {name}")
            else:
                self.stdout.write(f"  . Skipped (exists): {name}")

        created_b = 0
        for name, il, iw, ih, mw, cost in BOXES:
            _, created = Box.objects.get_or_create(
                name=name,
                defaults=dict(
                    inner_length=il, inner_width=iw, inner_height=ih,
                    max_weight=mw, cost=cost,
                ),
            )
            if created:
                created_b += 1
                self.stdout.write(f"  + Box: {name}")
            else:
                self.stdout.write(f"  . Skipped (exists): {name}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone — {created_p} product(s) and {created_b} box(es) added."
        ))
