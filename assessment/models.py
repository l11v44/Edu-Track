from django.db import models

from catalog import models as catalog
from main import models as main

# Create your models here.
class Assignment(models.Model):
    lesson = models.ForeignKey(catalog.Lesson, on_delete=models.CASCADE , related_name='assignments')
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lesson} - {self.title}"

status_choices = [
    ('Pending', 'Pending'),
    ('Graded', 'Graded')
]
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE , related_name='submissions')
    student = models.ForeignKey(main.User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/' , blank=True , null=True)
    text_content = models.TextField(blank=True , null=True)
    status = models.CharField(choices=status_choices, default='Pending', max_length=10)
    submitted_at = models.DateTimeField(auto_now_add=True)


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE , related_name='grade')
    teacher = models.ForeignKey(main.User, on_delete=models.SET_NULL, null=True)
    score = models.PositiveIntegerField(default=0)
    feedback = models.TextField(blank=True , null=True)
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.submission} - {self.teacher} - {self.score}"