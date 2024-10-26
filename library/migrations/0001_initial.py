# Generated by Django 4.2.3 on 2024-10-25 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
                ('publication_date', models.DateTimeField()),
                ('availability_status', models.BooleanField(default=True)),
                ('edition', models.CharField(max_length=50)),
                ('summary', models.TextField()),
            ],
        ),
    ]