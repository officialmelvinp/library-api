# Generated by Django 4.2.3 on 2024-10-26 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_remove_book_availability_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('title', 'author', 'genre', 'status', 'edition', 'summary', 'publication_date')},
        ),
    ]
