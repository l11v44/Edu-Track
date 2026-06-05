from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Grade
from main.tasks import send_grade_notification

@receiver(post_save, sender=Grade)
def grade_created(sender, instance, created, **kwargs):
    if created:
        send_grade_notification.delay(instance.id)



