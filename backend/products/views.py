from rest_framework import viewsets
import django_filters.rest_framework as filters
from .models import Product
from .serializers import ProductSerializer


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_rating = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    min_reviews = filters.NumberFilter(field_name='review_count', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'min_rating', 'min_reviews']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('-rating')
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
