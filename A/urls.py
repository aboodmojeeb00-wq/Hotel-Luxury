from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # First page is Login
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('user/', include('User.urls')),
    path('', include('hotel.urls')), # Includes welcome/, dashboard/ etc.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
