from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from health_app.models import Cart

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        Cart.objects.create(user=instance)