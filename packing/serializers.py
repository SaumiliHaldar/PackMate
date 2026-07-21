from rest_framework import serializers
from .models import Box, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'length', 'width', 'height', 'weight']

    def validate(self, data):
        for field in ['length', 'width', 'height', 'weight']:
            if data.get(field, 0) <= 0:
                raise serializers.ValidationError(
                    {field: f"{field} must be greater than 0."}
                )
        return data


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'name', 'inner_length', 'inner_width', 'inner_height',
                  'max_weight', 'cost']

    def validate(self, data):
        for field in ['inner_length', 'inner_width', 'inner_height', 'max_weight']:
            if data.get(field, 0) <= 0:
                raise serializers.ValidationError(
                    {field: f"{field} must be greater than 0."}
                )
        if data.get('cost', 0) < 0:
            raise serializers.ValidationError({'cost': "cost cannot be negative."})
        return data


class OrderItemInputSerializer(serializers.Serializer):
    """Used only for creating an order — validates each line item."""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Product {value} does not exist.")
        return value


class OrderCreateSerializer(serializers.Serializer):
    """Accepts a list of items and creates an Order + OrderItems."""
    items = OrderItemInputSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("An order must have at least one item.")
        # Check for duplicate product IDs in the same order
        ids = [item['product_id'] for item in value]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError(
                "Duplicate products in order — combine quantities instead."
            )
        return value

    def create(self, validated_data):
        order = Order.objects.create()
        for item in validated_data['items']:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity'],
            )
        return order


class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    recommended_box_name = serializers.CharField(source='recommended_box.name', read_only=True, default='Pending')

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'items', 'recommended_box_name']


class BoxRecommendationSerializer(serializers.ModelSerializer):
    """Returned by the recommend endpoint."""
    class Meta:
        model = Box
        fields = ['id', 'name', 'inner_length', 'inner_width', 'inner_height',
                  'max_weight', 'cost']
