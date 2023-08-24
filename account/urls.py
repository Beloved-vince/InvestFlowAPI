from django.urls import path, include
from account.views import RegisterViewSet
from rest_framework import routers
# from .views import verify_email


router = routers.DefaultRouter()
router.register(r'user', RegisterViewSet)

urlpatterns = [
    path('vi/api/', include(router.urls)),
    path('verify-email/', RegisterViewSet.as_view({'post': 'verify_email'}), name='verify-email'),
    # path('verify-email/', verify_email, name='verify-email'),

]