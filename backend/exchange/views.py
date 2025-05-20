from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Offer, Currency
from .serializers import OfferSerializer, CurrencySerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(offered_by=self.request.user)


