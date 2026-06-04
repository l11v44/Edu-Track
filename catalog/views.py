
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.db.models import Count, Q, F

from .forms import CourseForm
from .models import Course, Category, Lesson, LessonProgress

from django.core.exceptions import PermissionDenied

def teacher_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'T':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
from .forms import CourseForm , LessonForm
from django.db.models import Count
from django.contrib.auth import login as auth_login, logout

@login_required
def course_list(request):
    courses_to_show = Course.objects.filter(status='Published').annotate(students_count=Count('students')).order_by('-students_count')
    return render(request , 'catalog/course_list.html', {
        'courses': courses_to_show
    })


from django.db.models import Exists, OuterRef


@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.all().order_by('order')
    completed_lesson_ids = []
    if request.user.is_authenticated:
        completed_lesson_ids = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=course
        ).values_list('lesson_id', flat=True)
    for lesson in lessons:
        lesson.is_completed = lesson.id in completed_lesson_ids
    is_enrolled = course.students.filter(id=request.user.id).exists()
    return render(request, 'catalog/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled
    })


@login_required
def enroll_in_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course.students.add(request.user)
    messages.success(request, f"You successfully joined the course!!!: {course.title}")
    return redirect('course_detail', slug=slug)


@login_required
def my_courses(request):
    enrolled_courses = request.user.enrolled_courses.all()
    return render(request , 'main/profile.html', {
        'enrolled_courses': enrolled_courses
    })
@login_required
@teacher_required
def teacher_dashboard(request):
    courses = Course.objects.filter(author=request.user).annotate(students_count=Count('students'))
    return render(request , 'catalog/teacher_course_list.html', {
        'courses': courses,
    })



@login_required
def my_courses(request):
    enrolled_courses = request.user.enrolled_courses.all()
    return render(request , 'catalog/my_courses.html', {
        'enrolled_courses': enrolled_courses
    })


@login_required
@teacher_required
def course_create(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('course_list')
        else:
            print(form.errors)
    return render(request, 'catalog/course_form.html', {'form': form})


@login_required
@teacher_required
def create_lesson(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, author=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('teacher_dashboard')
    else:
        form = LessonForm()
    return render(request, 'catalog/lesson_form.html', {'form': form, 'course': course})

@login_required
@teacher_required
def course_update(request, slug):
    course = get_object_or_404(Course, slug=slug , author=request.user)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
        else:
            print(form.errors)
    return render(request, 'catalog/course_form.html', {'form': form})


@login_required
@teacher_required
def update_lesson(request, course_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, course__slug=course_slug, course__author=request.user, slug=lesson_slug)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'catalog/lesson_form.html', {'form': form})


@login_required
@teacher_required
def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug, author=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('teacher_dashboard')
    return render(request, 'catalog/course_confirm_delete.html', {'course': course})

@login_required
@teacher_required
def lesson_delete(request, course_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)
    if request.method == 'POST':
        lesson.delete()
        return redirect('teacher_dashboard')
    return render(request, 'catalog/lesson_confirm_delete.html', {'lesson': lesson})

@login_required
def get_lesson(request, course_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)
    return render(request, 'catalog/lesson_detail.html', {'lesson': lesson})


@login_required
def lesson_completed(request, course_slug, lesson_slug):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)

        if lesson.course.students.filter(id=request.user.id).exists():
            LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

        return redirect('course_detail', slug=course_slug)
    return redirect('course_detail', slug=course_slug)
