import django_filters
from .models import User
from django.db.models import Avg, Count

class ContractorFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(method='filter_by_rating', label="Min Average Rating")
    min_reviews = django_filters.NumberFilter(method='filter_by_reviews_count', label="Min Review Count")

    class Meta:
        model = User
        fields = []

    def filter_by_rating(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('reviews_received__rating')).filter(avg_rating__gte=value)

    def filter_by_reviews_count(self, queryset, name, value):
        return queryset.annotate(rev_count=Count('reviews_received')).filter(rev_count__gte=value)