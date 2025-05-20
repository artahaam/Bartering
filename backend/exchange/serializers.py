from rest_framework import serializers
from models import OfferProposal, Offer, Currency
from accounts.models import User


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
    to_give = CurrencySerializer(read_only=True)
    to_get = CurrencySerializer(read_only=True)
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

