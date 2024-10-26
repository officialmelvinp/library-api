# In config/urls.py
from django.contrib import admin
from django.urls import path, include
from library.routers import router  # Ensure the correct import

admin.site.site_header = "LIBRARY BY MELVINP"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # Ensure this path is correct
    
]
