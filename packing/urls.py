from django.urls import path
from .views import (
    BoxListCreateView,
    BoxRecommendView,
    OrderListCreateView,
    ProductListCreateView,
    index,
)

urlpatterns = [
    # Frontend
    path('', index, name='index'),

    # API
    path('products/', ProductListCreateView.as_view(), name='products'),
    path('boxes/', BoxListCreateView.as_view(), name='boxes'),
    path('orders/', OrderListCreateView.as_view(), name='orders'),
    path('orders/<int:pk>/recommend/', BoxRecommendView.as_view(), name='recommend'),
]
