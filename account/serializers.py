"""Serializer for the user model"""

from account.models import CustomUser
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class CustomUserSerializer(serializers.ModelSerializer):
    """Serialize the custom user model"""
    password = serializers.CharField(write_only=True)
    # phone_number = PhoneNumberField()
    # confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        """meta class for the custom user serializer"""
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password','phone_number', 'bvn','otp']
        
        
        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['phone_number'] = str(instance.phone_number)
            return representation

    def validate(self, attrs):
        """Validates that the passwords match"""
        password = attrs.get('password')
        # confirm_password = attrs.get('confirm_password')

        # if password != confirm_password:
        #     raise serializers.ValidationError("The two password fields did not match.")

        return attrs

    def create(self, validated_data):
        """creates and returns a user with encrypted password"""
        password = validated_data.pop('password')
        # validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        user.save()
        return user