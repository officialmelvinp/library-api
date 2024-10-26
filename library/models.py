from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    publication_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    edition = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    borrowed_by = models.CharField(max_length=255, blank=True, null=True)
    borrow_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('title', 'author', 'genre', 'status', 'edition', 'summary', 'publication_date')
        # This ensures that each combination of these fields is unique in the database.

    def save(self, *args, **kwargs):
        if not self.pk:  # Only check for duplicates on creation
            if Book.objects.filter(
                title=self.title,
                author=self.author,
                genre=self.genre,
                status=self.status,
                edition=self.edition,
                summary=self.summary,
                publication_date=self.publication_date
            ).exists():
                raise ValidationError("A book with these details already exists.")
        super().save(*args, **kwargs)
