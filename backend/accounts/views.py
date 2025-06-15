from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from .serializers import MyProfileSerializer, UserCreateSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from barter.models import Offer, Proposal
from barter.serializers import OfferSerializer, ProposalDetailSerializer
User = get_user_model()

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=True, methods=['get'])
    def offers(self, request, pk=None):

        user = self.get_object() 
        user_offers = user.offers.filter(status=Offer.Status.OPEN)
        serializer = OfferSerializer(user_offers, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def proposals(self, request, pk=None):
        user = self.get_object()
        if user != request.user:
            return Response(
                {'detail': 'You do not have permission to view these proposals.'},
                status=403
            )

        user_proposals = user.proposals.all()
        serializer = ProposalDetailSerializer(user_proposals, many=True, context={'request': request})
        return Response(serializer.data)
