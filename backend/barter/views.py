from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status 
from rest_framework.decorators import action 
from rest_framework.response import Response
from .serializers import OfferSerializer, TradeableSerializer, ProposalCreateSerializer, ProposalDetailSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import OfferFilter
from .models import Tradeable, Offer, Proposal
from comments.models import Comment  
from comments.serializers import CommentSerializer

class TradeableViewSet(viewsets.ModelViewSet):
    queryset = Tradeable.objects.all()
    serializer_class = TradeableSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.filter(status='open').order_by('-created_at')
    serializer_class = OfferSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = OfferFilter
    search_fields = ['title', 'description', 'to_get__name', 'to_give__name',]
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def proposals(self, request, pk=None):
        offer = self.get_object()
        proposals = offer.proposals.all()
        
        context = {'request': request}
        serializer = ProposalDetailSerializer(proposals, many=True, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def propose(self, request, pk=None):
        offer = self.get_object()
        
        if offer.status == Offer.Status.CLOSED:
            return Response({"detail": "Offer is no longer open."}, status=status.HTTP_400_BAD_REQUEST)
        # pass the status to the context so you can update the proposal's status in the serializer
        context = {'request': request, 'offer': offer}
        serializer = ProposalCreateSerializer(data=request.data, context=context)
        
        serializer.is_valid(raise_exception=True)
        new_proposal = serializer.save()

        read_serializer = ProposalDetailSerializer(new_proposal, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):

        offer = self.get_object() 

        if request.method == 'POST':
  
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=request.user, offer=offer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        comments = offer.comments.filter(parent__isnull=True) 
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    
    
class ProposalViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Proposal.objects.all()
    serializer_class = ProposalDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(methods=['post'], detail=True)
    def accept(self, request, pk=None):
        proposal = self.get_object()
        offer = proposal.offer
        
        if offer.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if offer.status != Offer.Status.OPEN:
            return Response(
                {'detail': 'This offer is already closed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        proposal.status = Proposal.Status.ACCEPTED
        proposal.save()


        # A better system should handle the status
        # ignored for now        
        offer.status = Offer.Status.CLOSED
        offer.save()

        offer.proposals.filter(status=Proposal.Status.PENDING).update(status=Proposal.Status.DECLINED)

        return Response({'status': 'proposal accepted and offer closed'})

    
    @action(methods=['post'], detail=True)
    def decline(self, request, pk=None):
        proposal = self.get_object()
        offer = proposal.offer
        
        if offer.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if offer.status != Offer.Status.OPEN:
            return Response(
                {'detail': 'This offer is already closed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        proposal.status = Proposal.Status.DECLINED
        proposal.save()

        return Response({'status': 'proposal declined'})

# class OfferViewSet(viewsets.ModelViewSet):
#     queryset = Offer.objects.all()
#     # serializer_class = OfferSerializer # Keep this as default for standard actions
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


