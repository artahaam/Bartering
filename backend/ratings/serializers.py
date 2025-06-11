from rest_framework import serializers
from .models import Rating
from django.utils.translation import gettext_lazy as _

from barter.models import Offer

class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.StringRelatedField(read_only=True)
    rated_user = serializers.StringRelatedField(read_only=True)
    offer = serializers.HyperlinkedRelatedField(view_name='barter:offer-detail', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'rater', 'rated_user', 'offer', 'score', 'review_text', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        offer = self.context['offer']
        rater = self.context['rater']
        rated_user = self.context['rated_user']

        if offer.status != Offer.Status.CLOSED:
            raise serializers.ValidationError(_("You can only rate completed trades."))

        if Rating.objects.filter(offer=offer, rater=rater, rated_user=rated_user).exists():
            raise serializers.ValidationError(_("You have already submitted a rating for this user on this offer."))

        return data
    
    def create(self, validated_data):
        offer = self.context['offer']
        rater = self.context['rater']
        rated_user = self.context['rated_user']
        return Rating.objects.create(
            offer=offer,
            rater=rater,
            rated_user=rated_user,
            **validated_data)