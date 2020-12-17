from django.urls import path
from .views import user_log,UserVerification,UserProfile
#from .views import send_json



urlpatterns= [
    path('log/<int:user_id>',user_log),
    path('login/',UserVerification.as_view(),name='user-login'),
    path('profile/',UserProfile.as_view(),name='user-profile'),
]