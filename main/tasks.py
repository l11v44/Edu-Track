from celery import shared_task
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL

@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Welcome to EduTrack',
        'Thank you for joining our platform.',
        DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )


from celery import shared_task
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL
from assessment.models import Grade

@shared_task
def send_grade_notification(grade_id):
    grade = Grade.objects.select_related('submission__student').get(id=grade_id)
    send_mail(
        'Your assignment has been graded',
        f'Hello, your grade is {grade.score}.',
        DEFAULT_FROM_EMAIL,
        [grade.submission.student.email],
        fail_silently=False,
    )


from celery import shared_task
from django.core.mail import send_mass_mail
from django.utils import timezone
from datetime import timedelta
from assessment.models import Assignment
from config.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_deadline_reminders():
    tomorrow = timezone.now().date() + timedelta(days=1)
    assignments = Assignment.objects.filter(deadline=tomorrow).select_related('lesson__course')

    messages = []
    for item in assignments:
        students = item.lesson.course.students.all()
        for student in students:
            messages.append((
                'Deadline Reminder',
                f'Assignment {item.title} is due tomorrow.',
                DEFAULT_FROM_EMAIL,
                [student.email]
            ))

    send_mass_mail(messages, fail_silently=False)