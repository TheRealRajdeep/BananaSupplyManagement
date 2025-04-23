from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/shipments/', include('shipments.urls')),  # This already exists
    path('api/ml/', include('ml.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # Add media URL configuration if needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)