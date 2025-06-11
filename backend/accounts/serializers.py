from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Avg 
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'phone_number', 
            'password', 
            'student_id', 
            'email',
            'first_name', 
            'last_name'
        )
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': False, 'allow_blank': True}}


    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=validated_data['password'],
            student_id=validated_data['student_id'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
        
        
class UserProfileSerializer(serializers.ModelSerializer):

    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'phone_number', 
            'email', 
            'student_id', 
            'first_name', 
            'last_name',
            'full_name',
            'average_rating',
             
        ]
        read_only_fields = ['phone_number', 'student_id', 'full_name']
        
        
    def get_average_rating(self, obj):
        avg = obj.received_ratings.aggregate(Avg('score')).get('score__avg')

        if avg is None:
            return "Not Rated Yet!"
        
        return round(avg, 1)