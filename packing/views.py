from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Box, Order, Product
from .selector import find_best_box
from .serializers import (
    BoxRecommendationSerializer,
    BoxSerializer,
    OrderCreateSerializer,
    OrderDetailSerializer,
    ProductSerializer,
)


# ── Products ────────────────────────────────────────────────────────────────

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer


# ── Boxes ───────────────────────────────────────────────────────────────────

class BoxListCreateView(generics.ListCreateAPIView):
    queryset = Box.objects.all().order_by('cost')
    serializer_class = BoxSerializer


# ── Orders ──────────────────────────────────────────────────────────────────

class OrderListCreateView(APIView):
    def get(self, request):
        orders = Order.objects.prefetch_related('items__product').order_by('-created_at')
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Calculate recommended box
            order_items = [
                {
                    'length':   item.product.length,
                    'width':    item.product.width,
                    'height':   item.product.height,
                    'weight':   item.product.weight,
                    'volume':   item.product.volume,
                    'quantity': item.quantity,
                }
                for item in order.items.select_related('product')
            ]
            boxes = [
                {
                    'id':           box.id,
                    'name':         box.name,
                    'inner_length': box.inner_length,
                    'inner_width':  box.inner_width,
                    'inner_height': box.inner_height,
                    'max_weight':   box.max_weight,
                    'inner_volume': box.inner_volume,
                    'cost':         float(box.cost),
                }
                for box in Box.objects.all()
            ]
            best = find_best_box(order_items, boxes)
            if best:
                order.recommended_box_id = best['id']
                order.save()

            return Response(
                OrderDetailSerializer(order).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Box Recommendation ───────────────────────────────────────────────────────

class BoxRecommendView(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.prefetch_related('items__product').get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'detail': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Build order_items list for the selector (no Django ORM inside selector)
        order_items = [
            {
                'length':   item.product.length,
                'width':    item.product.width,
                'height':   item.product.height,
                'weight':   item.product.weight,
                'volume':   item.product.volume,
                'quantity': item.quantity,
            }
            for item in order.items.all()
        ]

        if not order_items:
            return Response(
                {'detail': 'Order has no items.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Build boxes list for the selector
        boxes = [
            {
                'id':           box.id,
                'name':         box.name,
                'inner_length': box.inner_length,
                'inner_width':  box.inner_width,
                'inner_height': box.inner_height,
                'max_weight':   box.max_weight,
                'inner_volume': box.inner_volume,
                'cost':         float(box.cost),
            }
            for box in Box.objects.all()
        ]

        best = find_best_box(order_items, boxes)

        if best is None:
            return Response(
                {'detail': 'No suitable box found for this order.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        box_instance = Box.objects.get(pk=best['id'])
        return Response(BoxRecommendationSerializer(box_instance).data)


# ── Frontend ─────────────────────────────────────────────────────────────────

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def index(request):
    return render(request, 'packing/index.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
