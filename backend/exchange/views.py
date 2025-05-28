from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Offer, Currency
from .serializers import OfferSerializer, CurrencySerializer
from .permissions import IsOwnerOrReadOnly
from .filters import OfferFilter

# Create your views here.
class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_class = OfferFilter
    
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(offered_by=self.request.user)


