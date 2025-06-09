from rest_framework import serializers
from .models import Proposal, Offer, Tradeable
from accounts.models import User
from django.utils.translation import gettext_lazy as _ 


class TradeableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tradeable
        fields = [
            'id',
            'name',
            'description',
            'type',
        ]


class OfferSerializer(serializers.ModelSerializer):
    to_give = serializers.PrimaryKeyRelatedField(queryset=Tradeable.objects.all(), write_only=True)
    to_get = serializers.PrimaryKeyRelatedField(queryset=Tradeable.objects.all(), write_only=True)
    to_give_details = TradeableSerializer(source='to_give', read_only=True)
    to_get_details = TradeableSerializer(source='to_get', read_only=True)
    offered_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Offer
        fields = [
            'id',
            'offered_by',
            'status',
            'title',
            'description',
            'to_give',
            'to_get',
            'to_give_details',
            'to_get_details',
            'created_at',
        ]

class ProposalSerializer(serializers.ModelSerializer):
    proposer = serializers.PrimaryKeyRelatedField(read_only=True)
    offer = serializers.PrimaryKeyRelatedField(read_only=True)
    proposed_tradeable = TradeableSerializer(read_only=True)

    class Meta:
        model = Proposal
        fields = [
            'id',
            'offer',
            'proposer',
            'proposed_tradeable',
            'created_at',
        ]


class OfferProposalCreateSerializer(serializers.ModelSerializer):
    
    proposed_tradeable = serializers.PrimaryKeyRelatedField(
        queryset=Tradeable.objects.all(),
        required=True 
    )

    class Meta:
        model = Proposal
        fields = ['proposed_tradeable'] 

    def validate(self, data):
        
        offer = self.context.get('offer')
        request = self.context.get('request')

        if not offer or not request:
            raise serializers.ValidationError("Serializer requires 'offer' and 'request' in context.")

        if offer.offered_by == request.user:
            raise serializers.ValidationError(_("شما نمی‌توانید به آگهی خودتان پیشنهاد دهید."))

        if offer.status != Offer.Status.OPEN:
             raise serializers.ValidationError(_("این آگهی دیگر فعال نیست."))

        if Proposal.objects.filter(offer_id=offer, proposer_id=request.user).exists():
            raise serializers.ValidationError(_("شما قبلا برای این آگهی پیشنهاد داده‌اید."))

        return data

    def create(self, validated_data):

        offer = self.context['offer']
        proposer = self.context['request'].user

        proposal = Proposal.objects.create(
            offer=offer,
            proposer=proposer,
            **validated_data
        )
        return proposal

class OfferProposalViewSerializer(serializers.ModelSerializer):
    proposer = serializers.StringRelatedField() 
    proposed_tradeable = TradeableSerializer() 

    class Meta:
        model = Proposal
        fields = ['id', 'proposer', 'proposed_tradeable', 'created_at'] 