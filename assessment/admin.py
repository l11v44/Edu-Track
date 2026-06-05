from django.contrib import admin
from .models import Assignment, Submission, Grade

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'created_at')
    list_filter = ('created_at', 'lesson__course')
    search_fields = ('title', 'lesson__title')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('student__username', 'assignment__title')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('submission', 'teacher', 'score', 'graded_at')
    list_filter = ('score', 'graded_at')
    search_fields = ('submission__student__username', 'teacher__username')