from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status 
from rest_framework.decorators import action 
from rest_framework.response import Response
from .serializers import OfferSerializer, CurrencySerializer, OfferProposalCreateSerializer, OfferProposalViewSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import OfferFilter
from .models import Currency, Offer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

# class OfferViewSet(viewsets.ModelViewSet):
#     queryset = Offer.objects.all()
#     serializer_class = OfferSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     filterset_class = OfferFilter
    
#     search_fields = ['title', 'description']
#     ordering_fields = ['created_at', 'title']
#     ordering = ['-created_at']

#     def perform_create(self, serializer):
#         serializer.save(offered_by=self.request.user)


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


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def propose(self, request, pk=None):
        
        offer = self.get_object() 
      
        context = {'request': request, 'offer': offer}

        serializer = OfferProposalCreateSerializer(data=request.data, context=context)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def proposals(self, request, pk=None):
        offer = self.get_object()
        
        if offer.offered_by != request.user:
            return Response({"detail": "Not authorized to view proposals."}, status=status.HTTP_403_FORBIDDEN)

        proposals = offer.proposals.all() 
        serializer = OfferProposalViewSerializer(proposals, many=True)
        return Response(serializer.data)
