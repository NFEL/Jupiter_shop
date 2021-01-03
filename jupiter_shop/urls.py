from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import debug_toolbar
# from .views import Landing



urlpatterns = [
    path('admin/', admin.site.urls),
    path('stores/', include('store.urls')),
    path('user/',include('user.urls')),
    
    path('cart/',include('pardakht.urls')),
    
    path('', include('product.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

