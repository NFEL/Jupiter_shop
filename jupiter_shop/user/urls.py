from django.urls import path
from .views import user_log
#from .views import send_json



urlpatterns= [
    path('log/<int:user_id>',user_log)
]