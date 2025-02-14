from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Empleado

@receiver(post_save, sender=User)
def create_empleado(sender, instance, created, **kwargs):
    if created:
        Empleado.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_empleado(sender, instance, **kwargs):
    instance.empleado.save()