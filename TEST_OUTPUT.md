# PackMate - Test Output

**Command run:**
```bash
python manage.py test packing.tests --verbosity=2
```

**Output:**
```text
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Found 25 test(s).
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles
  Apply all migrations: admin, auth, contenttypes, packing, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying packing.0001_initial... OK
  Applying packing.0002_order_recommended_box_order_status_product_is_active_and_more... OK
  Applying packing.0003_remove_order_recommended_box_remove_order_status_and_more... OK
  Applying packing.0004_order_recommended_box... OK
  Applying sessions.0001_initial... OK
test_create_box (packing.tests.test_api.BoxAPITests.test_create_box) ... ok
test_create_box_zero_dimension_rejected (packing.tests.test_api.BoxAPITests.test_create_box_zero_dimension_rejected) ... ok
test_create_order (packing.tests.test_api.OrderAPITests.test_create_order) ... ok
test_create_order_duplicate_products_rejected (packing.tests.test_api.OrderAPITests.test_create_order_duplicate_products_rejected) ... ok
test_create_order_empty_items_rejected (packing.tests.test_api.OrderAPITests.test_create_order_empty_items_rejected) ... ok
test_create_order_invalid_product_rejected (packing.tests.test_api.OrderAPITests.test_create_order_invalid_product_rejected) ... ok
test_create_order_zero_quantity_rejected (packing.tests.test_api.OrderAPITests.test_create_order_zero_quantity_rejected) ... ok
test_list_orders (packing.tests.test_api.OrderAPITests.test_list_orders) ... ok
test_create_product (packing.tests.test_api.ProductAPITests.test_create_product) ... ok
test_create_product_negative_weight_rejected (packing.tests.test_api.ProductAPITests.test_create_product_negative_weight_rejected) ... ok
test_create_product_zero_dimension_rejected (packing.tests.test_api.ProductAPITests.test_create_product_zero_dimension_rejected) ... ok
test_list_products (packing.tests.test_api.ProductAPITests.test_list_products) ... ok
test_recommend_404_for_nonexistent_order (packing.tests.test_api.RecommendAPITests.test_recommend_404_for_nonexistent_order) ... ok
test_recommend_404_when_no_box_fits (packing.tests.test_api.RecommendAPITests.test_recommend_404_when_no_box_fits) ... ok
test_recommend_returns_cheapest_valid_box (packing.tests.test_api.RecommendAPITests.test_recommend_returns_cheapest_valid_box) ... ok
test_empty_order_returns_none (packing.tests.test_selector.SelectorFitTests.test_empty_order_returns_none) ... ok
test_heavy_order_skips_small_box (packing.tests.test_selector.SelectorFitTests.test_heavy_order_skips_small_box) ... ok
test_item_too_large_returns_none (packing.tests.test_selector.SelectorFitTests.test_item_too_large_returns_none) ... ok
test_long_thin_item_fails_dimension_check (packing.tests.test_selector.SelectorFitTests.test_long_thin_item_fails_dimension_check) ... ok
test_multiple_items_picks_correct_box (packing.tests.test_selector.SelectorFitTests.test_multiple_items_picks_correct_box) ... ok
test_no_boxes_returns_none (packing.tests.test_selector.SelectorFitTests.test_no_boxes_returns_none) ... ok
test_picks_cheapest_valid_box (packing.tests.test_selector.SelectorFitTests.test_picks_cheapest_valid_box) ... ok
test_single_item_fits_smallest_box (packing.tests.test_selector.SelectorFitTests.test_single_item_fits_smallest_box) ... ok
test_total_weight_exceeds_all_boxes_returns_none (packing.tests.test_selector.SelectorFitTests.test_total_weight_exceeds_all_boxes_returns_none) ... ok
test_volume_overflow_returns_none (packing.tests.test_selector.SelectorFitTests.test_volume_overflow_returns_none) ... ok

----------------------------------------------------------------------
Ran 25 tests in 0.052s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
System check identified no issues (0 silenced).
```

