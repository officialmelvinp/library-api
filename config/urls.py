# In config/urls.py
from django.contrib import admin
from django.urls import path, include
from library.routers import router  # Ensure the correct import
from django.views.generic import RedirectView

admin.site.site_header = "LIBRARY BY MELVINP"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/api/v1/', permanent=False)),  # Redirect root to API
    path('api/v1/', include(router.urls)),
]
