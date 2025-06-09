from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status 
from rest_framework.decorators import action 
from rest_framework.response import Response
from .serializers import OfferSerializer, TradeableSerializer, OfferProposalCreateSerializer, OfferProposalViewSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import OfferFilter
from .models import Tradeable, Offer


class TradeableViewSet(viewsets.ModelViewSet):
    queryset = Tradeable.objects.all()
    serializer_class = TradeableSerializer
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

# backend/barter/views.py
# ... (other imports) ...
from .serializers import OfferSerializer, TradeableSerializer, OfferProposalCreateSerializer, OfferProposalViewSerializer # Ensure all are imported

# ... TradeableViewSet ...

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    # serializer_class = OfferSerializer # Keep this as default for standard actions
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    # --- ADD THIS METHOD ---
    def get_serializer_class(self):
        if self.action == 'propose':
            return OfferProposalCreateSerializer
        elif self.action == 'proposals': # If you want to use OfferProposalViewSerializer for the list
            return OfferProposalViewSerializer
        return OfferSerializer # Default for list, retrieve, create, update, etc.
    # --- END OF ADDED METHOD ---

    def perform_create(self, serializer): # This uses OfferSerializer
        serializer.save(offered_by=self.request.user)

    @action(detail=True, methods=['post']
            , permission_classes=[permissions.IsAuthenticated]
            )
    def propose(self, request, pk=None):
        offer = self.get_object()
        context = {'request': request, 'offer': offer}
        # The serializer instance will now be correctly inferred by DRF for form rendering too
        serializer = self.get_serializer(data=request.data, context=context)
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
        
        proposals_queryset = offer.proposals.all()
        # Use get_serializer for consistency
        serializer = self.get_serializer(proposals_queryset, many=True)
        return Response(serializer.data)