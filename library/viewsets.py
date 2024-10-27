from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'title': ['icontains'],
        'author': ['icontains'],
        'genre': ['icontains'],
        'publication_date': ['exact'],
        'status': ['exact'],
        'edition': ['icontains'],
        'summary': ['icontains']
    }

    def create(self, request):
        serializer = BookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            status_value = serializer.validated_data.get('status')
            if status_value in ['lost', 'damaged']:
                return Response({
                    "status": "Error",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Cannot create a book with 'lost' or 'damaged' status",
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                serializer.save()
                return Response({
                    "status": "Success",
                    "code": status.HTTP_201_CREATED,
                    "message": "Book added successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            except transaction.TransactionManagementError as e:
                return Response({
                    "status": "Error",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e),
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check if the error is due to 'lost' or 'damaged' status
            status_value = request.data.get('status')
            if status_value in ['lost', 'damaged']:
                return Response({
                    "status": "Error",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Cannot create a book with 'lost' or 'damaged' status",
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                "status": "Error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Book creation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    # ... (rest of the methods remain unchanged)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            updated_status = serializer.validated_data.get('status')
            if updated_status in ['lost', 'damaged']:
                instance.delete()
                return Response({
                    "status": "Success",
                    "code": status.HTTP_204_NO_CONTENT,
                    "message": "Book deleted successfully"
                }, status=status.HTTP_204_NO_CONTENT)

            self.perform_update(serializer)
            return Response({
                "status": "Success",
                "code": status.HTTP_200_OK,
                "message": "Book updated successfully",
                "data": serializer.data
            })
        else:
            return Response({
                "status": "Error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Book update failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        params = request.query_params
        non_empty_params = {k: v for k, v in params.items() if v.strip()}

        if params and not non_empty_params:
            return Response({
                "status": "Error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "At least one non-empty search parameter is required.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        if not params:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "status": "Success",
                "code": status.HTTP_200_OK,
                "message": "All books retrieved successfully",
                "data": serializer.data
            })

        queryset = self.get_queryset()
        for key, value in non_empty_params.items():
            if key == 'title':
                queryset = queryset.filter(title__icontains=value)
            elif key == 'author':
                queryset = queryset.filter(author__icontains=value)
            elif key == 'genre':
                queryset = queryset.filter(genre__icontains=value)
            elif key == 'publication_date':
                queryset = queryset.filter(publication_date=value)
            elif key == 'status':
                queryset = queryset.filter(status=value)
            elif key == 'edition':
                queryset = queryset.filter(edition__icontains=value)
            elif key == 'summary':
                queryset = queryset.filter(summary__icontains=value)

        if not queryset.exists():
            return Response({
                "status": "Error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": "No books found matching the provided filters.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "Books retrieved successfully",
            "data": serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "Book retrieved successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "status": "Success",
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Book deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)