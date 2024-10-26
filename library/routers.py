from rest_framework import routers
from .viewsets import BookViewSet

app_name = "library"

router = routers.DefaultRouter()
router.register('books', BookViewSet, basename='book')