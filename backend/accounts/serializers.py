from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'phone_number', 
            'password', 
            'email', 
            'student_id', 
            'first_name', 
            'last_name'
        )
        extra_kwargs = {'password': {'write_only': True}}
        
        
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
    class Meta:
        model = User
        fields = [
            'phone_number', 
            'email', 
            'student_id', 
            'first_name', 
            'last_name',
            'full_name', 
        ]
        read_only_fields = ['phone_number', 'student_id', 'full_name']