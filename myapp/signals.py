# ✅ File: myapp/signals.py

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import Profile


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """
    Automatically creates a Profile when a new User is created.
    Superusers get 'admin' role, normal users get 'emp'.
    """
    if created and not hasattr(instance, 'profile'):
        role = 'admin' if instance.is_superuser else 'emp'
        Profile.objects.create(user=instance, role=role)