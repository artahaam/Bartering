from rest_framework import serializers
from .models import OfferProposal, Offer, Currency
from accounts.models import User
from django.utils.translation import gettext_lazy as _ 


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            'id',
            'name',
            'description',
            'is_item',
            'is_service',
        ]


class OfferSerializer(serializers.ModelSerializer):
    to_give = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), write_only=True)
    to_get = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), write_only=True)
    to_give_details = CurrencySerializer(source='to_give', read_only=True)
    to_get_details = CurrencySerializer(source='to_get', read_only=True)
    offered_by = serializers.PrimaryKeyRelatedField(read_only=True)
    accepted_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Offer
        fields = [
            'id',
            'offered_by',
            'accepted_by',
            'status',
            'title',
            'description',
            'to_give',
            'to_get',
            'to_give_details',
            'to_get_details',
            'created_at',
        ]

class OfferProposalSerializer(serializers.ModelSerializer):
    proposer_id = serializers.PrimaryKeyRelatedField(read_only=True)
    offer_id = serializers.PrimaryKeyRelatedField(read_only=True)
    proposed_currency = CurrencySerializer(read_only=True)

    class Meta:
        model = OfferProposal
        fields = [
            'id',
            'offer_id',
            'proposer_id',
            'proposed_currency',
            'created_at',
        ]


class OfferProposalCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used ONLY for CREATING a new OfferProposal.
    It expects 'proposed_currency' (as ID) in the input.
    'offer' and 'proposer' are set automatically in the view.
    """
    
    proposed_currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        required=True 
    )

    class Meta:
        model = OfferProposal
        fields = ['proposed_currency'] 

    def validate(self, data):
        
        offer = self.context.get('offer')
        request = self.context.get('request')

        if not offer or not request:
            raise serializers.ValidationError("Serializer requires 'offer' and 'request' in context.")

        if offer.offered_by == request.user:
            raise serializers.ValidationError(_("شما نمی‌توانید به آگهی خودتان پیشنهاد دهید."))

        if offer.status != Offer.Status.OPEN:
             raise serializers.ValidationError(_("این آگهی دیگر فعال نیست."))

        if OfferProposal.objects.filter(offer_id=offer, proposer_id=request.user).exists():
            raise serializers.ValidationError(_("شما قبلا برای این آگهی پیشنهاد داده‌اید."))

        return data

    def create(self, validated_data):

        offer = self.context['offer']
        proposer = self.context['request'].user

        proposal = OfferProposal.objects.create(
            offer_id=offer,
            proposer_id=proposer,
            **validated_data
        )
        return proposal

class OfferProposalViewSerializer(serializers.ModelSerializer):
    proposer = serializers.StringRelatedField() 
    proposed_currency = CurrencySerializer() 

    class Meta:
        model = OfferProposal
        fields = ['id', 'proposer', 'proposed_currency', 'created_at'] 