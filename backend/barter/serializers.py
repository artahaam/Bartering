from rest_framework import serializers
from .models import Proposal, Offer, Tradeable
from accounts.models import User
from comments.models import Comment
from django.utils.translation import gettext_lazy as _ 


class TradeableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tradeable
        fields = [
            'name',
            'description',
            'type',
            'image',
        ]


class OfferSerializer(serializers.ModelSerializer):
    to_give = TradeableSerializer()
    to_get = TradeableSerializer()
    comments = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='text'
     )
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Offer
        fields = [
            'id',
            'owner',
            'status',
            'title',
            'description',
            'to_give',
            'to_get',
            'comments',
            'created_at',
        ]
    def create(self, validated_data):
        
        to_give_data = validated_data.pop('to_give')
        to_get_data = validated_data.pop('to_get')

        to_give = Tradeable.objects.create(**to_give_data)
        to_get = Tradeable.objects.create(**to_get_data)

        offer = Offer.objects.create(
            to_give=to_give,
            to_get=to_get,
            **validated_data
        )
        return offer
    
    
    def update(self, instance, validated_data):

        to_give_data = validated_data.pop('to_give', None)
        to_get_data = validated_data.pop('to_get', None)

        if to_give_data:
            to_give_instance = instance.to_give
            for attr, value in to_give_data.items():
                setattr(to_give_instance, attr, value)
            to_give_instance.save()

        if to_get_data:
            to_get_instance = instance.to_get
            for attr, value in to_get_data.items():
                setattr(to_get_instance, attr, value)
            to_get_instance.save()

        instance = super().update(instance, validated_data)
        return instance


class ProposalDetailSerializer(serializers.ModelSerializer):
    proposer = serializers.HyperlinkedRelatedField(
        view_name='accounts:user-detail',
        read_only=True
    )
    offer = serializers.HyperlinkedRelatedField(
        view_name='barter:offer-detail',
        read_only=True
    )
    proposed_tradeable = TradeableSerializer(read_only=True)

    class Meta:
        model = Proposal
        fields = [
            'id',
            'offer',
            'proposer',
            'proposed_tradeable',
            'status',
            'created_at',
        ]


class ProposalCreateSerializer(serializers.ModelSerializer):
    
    proposed_tradeable = TradeableSerializer()

    class Meta:
        model = Proposal
        fields = ['proposed_tradeable'] 

    def validate(self, data):
        
        offer = self.context.get('offer')
        request = self.context.get('request')
        
        if not offer or not request:
            raise serializers.ValidationError("Serializer requires 'offer' and 'request' in context.")

        if offer.owner == request.user:
            raise serializers.ValidationError(_("شما نمی‌توانید به آگهی خودتان پیشنهاد دهید."))

        if offer.status != Offer.Status.OPEN:
             raise serializers.ValidationError(_("این آگهی دیگر فعال نیست."))

        if Proposal.objects.filter(offer_id=offer, proposer_id=request.user).exists():
            raise serializers.ValidationError(_("شما قبلا برای این آگهی پیشنهاد داده‌اید."))

        return data

    def create(self, validated_data):
        # add status
        proposed_tradeable_data = validated_data.pop('proposed_tradeable')
        proposed_tradeable = Tradeable.objects.create(**proposed_tradeable_data)

        offer = self.context['offer']
        proposer = self.context['request'].user

        proposal = Proposal.objects.create(
            offer=offer,
            proposer=proposer,
            proposed_tradeable=proposed_tradeable,
            **validated_data
        )
        return proposal

