
from celery import shared_task

@shared_task
def send_verification_email(user_email, code):
    send_mail(
        subject='Your Verification Code for EduTrack',
        message=f'Welcome to EduTrack! Your verification code is: {code}',
        from_email='EduTrack <vlad2511k@gmail.com>',
        recipient_list=[user_email],
        fail_silently=False,
    )


from celery import shared_task
from django.core.mail import send_mail
from assessment.models import Grade

@shared_task
def send_grade_notification(grade_id , user_email):
    grade = Grade.objects.select_related('submission__student').get(id=grade_id)
    send_mail(
        subject='Welcome to EduTrack',
        message='Thank you for joining our platform.',
        from_email='vlad2511k@gmail.com',
        recipient_list=[user_email],
        fail_silently=False,
    )


from celery import shared_task
from django.core.mail import send_mass_mail
from django.utils import timezone
from datetime import timedelta
from assessment.models import Assignment
from config.settings import DEFAULT_FROM_EMAIL


