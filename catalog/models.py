from django.db import models
from django.utils.text import slugify
STATUS_CHOICES = [
    ('Draft', 'Draft'),
    ('Published', 'Published'),
]



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    author = models.ForeignKey('main.User', on_delete=models.CASCADE, related_name='courses', default=1)
    students = models.ManyToManyField('main.User', related_name='enrolled_courses', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(blank=True, null=True)
    content = models.TextField()
    slug = models.SlugField(unique=False, blank=True)
    video_url = models.URLField(help_text="Paste YouTube video link here")

    class Meta:
        unique_together = ('course', 'slug')
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = slug if slug else f"lesson-{self.order}"
        if not self.order:
            last_lesson = Lesson.objects.filter(course=self.course).order_by('-order').first()
            if last_lesson:
                self.order = last_lesson.order + 1
            else:
                self.order = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}. {self.title}"


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progresses')
    user = models.ForeignKey('main.User', on_delete=models.CASCADE, related_name='progresses')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} - {self.lesson}"
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Course)
def clear_course_cache(sender, **kwargs):
    cache.clear()
