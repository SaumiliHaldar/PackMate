"""
selector.py — Pure box selection logic. No Django imports.

Algorithm (Option A — conservative approximation):
  For each candidate box, three checks must ALL pass:
    1. Weight: box.max_weight >= total_weight of order
    2. Per-item dimension check: every product must physically fit inside the box
       (sorted dimension comparison, catches long-thin-item edge case)
    3. Volume guard: sum of all item volumes <= box inner volume
       (catches "too many items" case)

  From all passing boxes, return the one with the lowest cost.
  Returns None if no box qualifies.

Note: This is a conservative approximation, not true 3D bin-packing (NP-hard).
"""


def find_best_box(order_items, boxes):
    """
    Params:
        order_items: list of dicts, each with:
            {
                'length': float,  # cm
                'width':  float,  # cm
                'height': float,  # cm
                'weight': float,  # kg
                'volume': float,  # cm³
                'quantity': int,
            }
        boxes: list of dicts, each with:
            {
                'id':           int,
                'name':         str,
                'inner_length': float,  # cm
                'inner_width':  float,  # cm
                'inner_height': float,  # cm
                'max_weight':   float,  # kg
                'inner_volume': float,  # cm³
                'cost':         float,
            }

    Returns:
        The box dict with the lowest cost that satisfies all checks,
        or None if no box qualifies.
    """
    if not order_items:
        return None

    # --- Pre-compute order totals ---
    total_weight = sum(item['weight'] * item['quantity'] for item in order_items)
    total_volume = sum(item['volume'] * item['quantity'] for item in order_items)

    valid_boxes = []

    for box in boxes:
        box_dims = sorted([box['inner_length'], box['inner_width'], box['inner_height']])

        # Check 1: weight
        if box['max_weight'] < total_weight:
            continue

        # Check 2: per-item dimension fit
        all_fit = True
        for item in order_items:
            item_dims = sorted([item['length'], item['width'], item['height']])
            if not (
                item_dims[0] <= box_dims[0]
                and item_dims[1] <= box_dims[1]
                and item_dims[2] <= box_dims[2]
            ):
                all_fit = False
                break
        if not all_fit:
            continue

        # Check 3: volume guard
        if total_volume > box['inner_volume']:
            continue

        valid_boxes.append(box)

    if not valid_boxes:
        return None

    return min(valid_boxes, key=lambda b: b['cost'])
