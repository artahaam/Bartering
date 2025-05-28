from django_filters import rest_framework as filters
from .models import Offer, Currency

class OfferFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=Offer.Status.choices)
    to_give_id = filters.NumberFilter(field_name='to_give__id')
    to_get_id = filters.NumberFilter(field_name='to_get__id')
    offered_by_id = filters.NumberFilter(field_name='offered_by__id')

    class Meta:
        model = Offer
        fields = ['title', 'status', 'to_give_id', 'to_get_id', 'offered_by_id']