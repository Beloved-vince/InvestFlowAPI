from django.urls import path, include
from account.views import RegisterViewSet, VerifyUserViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'user', RegisterViewSet,)

urlpatterns = [
    path('', include(router.urls)),
    path('verify-email', VerifyUserViewSet.as_view({'post': 'verify_email'}), name='verify-email'),

  
]