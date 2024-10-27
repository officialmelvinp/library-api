from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book

class BookViewSetTests(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            genre="Fiction",
            publication_date="2024-01-01",
            status="available",
            edition="First Edition",
            summary="This is a summary of Book One."
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            genre="Non-Fiction",
            publication_date="2024-02-01",
            status="borrowed",
            edition="Second Edition",
            summary="This is a summary of Book Two."
        )

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            "title": "New Book",
            "author": "New Author",
            "genre": "Mystery",
            "publication_date": "2024-03-01",
            "status": "available",
            "edition": "First Edition",
            "summary": "This is a summary of the new book."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['title'], "New Book")

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], self.book1.title)

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            "title": "Updated Book",
            "status": "borrowed",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")
        self.assertEqual(self.book1.status, "borrowed")

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_update(self):
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            "title": "",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_filter_books(self):
        url = reverse('book-list') + '?status=available'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['title'], "Book One")

    def test_no_books_found(self):
        url = reverse('book-list') + '?title=Nonexistent Book'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "No books found matching the provided filters.")

    # New test methods

    def test_update_book_to_lost_status(self):
        """Test updating a book's status to 'lost' results in deletion"""
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            "status": "lost",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Expecting 204 since it is deleted
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_update_book_to_damaged_status(self):
        """Test updating a book's status to 'damaged' results in deletion"""
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            "status": "damaged",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Expecting 204 since it is deleted
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_create_book_with_lost_status(self):
        """Test creating a book with 'lost' status is not allowed"""
        url = reverse('book-list')
        data = {
            "title": "Lost Book",
            "author": "Author",
            "genre": "Fiction",
            "publication_date": "2024-01-01",
            "status": "lost",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot create a book with 'lost' or 'damaged' status", str(response.data['message']))

    def test_create_book_with_damaged_status(self):
        """Test creating a book with 'damaged' status is not allowed"""
        url = reverse('book-list')
        data = {
            "title": "Damaged Book",
            "author": "Author",
            "genre": "Fiction",
            "publication_date": "2024-01-01",
            "status": "damaged",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot create a book with 'lost' or 'damaged' status", str(response.data['message']))
