from django.contrib import admin
from .models import Category, Course, Lesson, LessonProgress
@admin.action(description='Mark selected courses as Published')
def make_published(modeladmin, request, queryset):
    queryset.update(status='Published')

@admin.action(description='Export student emails to CSV')
def export_students_emails(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email'])
    for course in queryset:
        for student in course.students.all():
            writer.writerow([student.email])
    return response

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'category', 'price', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description')
    actions = [make_published, export_students_emails]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)
    ordering = ('course', 'order')

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'date')
    list_filter = ('date', 'lesson')
    search_fields = ('user__username', 'lesson__title')