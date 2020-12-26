from django.urls import path
from .views import UserVerification, UserProfile, logout_user, receive_user_uuid

urlpatterns = [
    path('login/', UserVerification.as_view(), name='user-login'),
    path('logout/', logout_user, name='user-logout'),
    path('profile/', UserProfile.as_view(), name='user-profile'),
    path('verificationcode/<str:user_uuid>',
         receive_user_uuid, name='verification'),
]
