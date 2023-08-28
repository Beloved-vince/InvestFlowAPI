from django.shortcuts import render
from account.models import CustomUser
from account.serializers import CustomUserSerializer, VerifyUserSerializer
from rest_framework_swagger.views import get_swagger_view
from rest_framework import viewsets, status
from account.emails import send_otp_via_email
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.contrib.auth import authenticate, login, logout
from drf_yasg.utils import swagger_auto_schema

# schema_view = get_swagger_view(title='Pastebin API')

# urlpatterns = [
#     url(r'^$', schema_view)
# ]

class RegisterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for registering user accounts.
    parameters:
        firstname: maximum of 50 characters
        lastname: maximum of 50 characters
        email: valid email address for verification
        bvn: valid bank verification number
        phone number: country code format
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_description="Authenticate Admin using email and password"
    )
    
    
    def perform_create(self, serializer):
        """OTP verification and validation"""

        user_instance = serializer.save()
        send_otp_via_email(user_instance.email)



class VerifyUserViewSet(viewsets.ViewSet):
    
    @swagger_auto_schema(
        request_body=VerifyUserSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_description="Verify user with valid email"
    )
    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        """
        Verify email by getting the otp sent to the email from the client view
        """
        serializer = VerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            print(user)
        except (CustomUser.DoesNotExist, AttributeError, ValueError) as e:
            return Response({'error': f'Email not found {e}'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)



