from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Book

@receiver(pre_save, sender=Book)
def handle_book_status_change(sender, instance, **kwargs):
    if instance.pk:  # This check ensures the book already exists (for updates)
        try:
            old_instance = Book.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                if instance.status in ['lost', 'damaged']:
                    print(f"Book '{instance.title}' status changed to {instance.status}. It will be deleted.")
                    # We'll handle the deletion in post_save to ensure this message is printed
                else:
                    print(f"Book '{instance.title}' status updated from {old_instance.status} to {instance.status}.")
        except Book.DoesNotExist:
            pass  # This can happen if the book is new
    else:
        if instance.status in ['lost', 'damaged']:
            print(f"Attempted to create a new book '{instance.title}' with status: {instance.status}. Creation prevented.")
            raise transaction.TransactionManagementError("Cannot create a book with 'lost' or 'damaged' status.")
        else:
            print(f"New book '{instance.title}' is being created with status: {instance.status}")

@receiver(post_save, sender=Book)
def book_saved(sender, instance, created, **kwargs):
    if created:
        print(f"New book '{instance.title}' has been created with status: {instance.status}")
    else:
        if instance.status in ['lost', 'damaged']:
            print(f"Book '{instance.title}' status changed to {instance.status}. Deleting the book.")
            instance.delete()
        else:
            print(f"Book '{instance.title}' has been updated. Current status: {instance.status}")

@receiver(post_delete, sender=Book)
def book_deleted(sender, instance, **kwargs):
    print(f"Book '{instance.title}' has been deleted.")