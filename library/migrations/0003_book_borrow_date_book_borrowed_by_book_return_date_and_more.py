# Generated by Django 4.2.3 on 2024-10-26 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_book_publication_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='borrow_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='borrowed_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]