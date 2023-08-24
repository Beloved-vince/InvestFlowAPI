from django.shortcuts import render
from account.models import CustomUser
from account.serializers import CustomUserSerializer
from rest_framework_swagger.views import get_swagger_view
from rest_framework import viewsets, status
from account.emails import send_otp_via_email
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
# schema_view = get_swagger_view(title='Pastebin API')

# urlpatterns = [
#     url(r'^$', schema_view)
# ]

class RegisterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for registering user accounts and email verification.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def perform_create(self, serializer):
        """OTP verification and validation"""

        user_instance = serializer.save()
        send_otp_via_email(user_instance.email)


    def verify_email(self, request):
        """Verify email by getting the otp sent to the email from the client view"""
        
        input_otp = request.data.get('otp')
        print(input_otp)        
        get_email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=get_email)
            print(user)
        except (CustomUser.DoesNotExist, AttributeError, ValueError) as e:
            return Response({'error': f'Email not found {e}'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == input_otp:
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
    def login_view(self, request):
        """Login endpoint"""
        username = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            return Response(
                {"message": "Authentication successful"}
            )
        else:
            return Response(
                {"error": "Invalid credentials"}
            )