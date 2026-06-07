from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.db.models import Count, Q, F

from .forms import CourseForm
from .models import Course, Category, Lesson, LessonProgress

from django.core.exceptions import PermissionDenied

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'T'
from .forms import CourseForm , LessonForm

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from .models import Course

#@method_decorator(cache_page(60 * 15), name='dispatch')
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'catalog/course_list.html'
    context_object_name = 'courses'
    def get_queryset(self):
        return Course.objects.filter(status='Published') \
            .annotate(students_count=Count('students')) \
            .order_by('-students_count')


from django.db.models import Exists, OuterRef

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'catalog/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object

        lessons = course.lessons.all().order_by('order')

        completed_ids = LessonProgress.objects.filter(
            user=self.request.user,
            lesson__course=course
        ).values_list('lesson_id', flat=True)

        for lesson in lessons:
            lesson.is_completed = lesson.id in completed_ids

        context['lessons'] = lessons
        context['is_enrolled'] = course.students.filter(id=self.request.user.id).exists()

        return context



from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class EnrollInCourseView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Course

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        messages.success(request, f"You successfully joined the course!!!: {course.title}")
        return redirect('course_detail', slug=course.slug)


from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class MyCoursesView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'main/profile.html'
    context_object_name = 'enrolled_courses'

    def get_queryset(self):
        return self.request.user.enrolled_courses.all()


class TeacherDashboardView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Course
    template_name = 'catalog/teacher_course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.filter(author=self.request.user).annotate(
            students_count=Count('students')
        )





from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class MyCoursesView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'catalog/my_courses.html'
    context_object_name = 'enrolled_courses'

    def get_queryset(self):
        return self.request.user.enrolled_courses.all()


from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class CourseCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'catalog/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

from django.views.generic import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

class LessonCreateView(LoginRequiredMixin, TeacherRequiredMixin,CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'catalog/lesson_form.html'
    success_url = reverse_lazy('teacher_dashboard')

    def get(self, request, *args, **kwargs):
        self.object = None
        self.course = self.get_course()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.course = self.get_course()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs['course_slug'], author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

class CourseUpdateView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'catalog/course_form.html'
    success_url = reverse_lazy('course_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Course, slug=self.kwargs['slug'], author=self.request.user)


from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

class LessonUpdateView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'catalog/lesson_form.html'
    success_url = reverse_lazy('teacher_dashboard')

    def get_object(self, queryset=None):
        return get_object_or_404(
            Lesson,
            course__slug=self.kwargs['course_slug'],
            course__author=self.request.user,
            slug=self.kwargs['lesson_slug']
        )

from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

class CourseDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = Course
    template_name = 'catalog/course_confirm_delete.html'
    success_url = reverse_lazy('teacher_dashboard')

    def get_object(self, queryset=None):
        return get_object_or_404(Course, slug=self.kwargs['slug'], author=self.request.user)

from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

class LessonDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = Lesson
    template_name = 'catalog/lesson_confirm_delete.html'
    success_url = reverse_lazy('teacher_dashboard')

    def get_object(self, queryset=None):
        return get_object_or_404(
            Lesson,
            course__slug=self.kwargs['course_slug'],
            course__author=self.request.user,
            slug=self.kwargs['lesson_slug']
        )


from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'catalog/lesson_detail.html'
    context_object_name = 'lesson'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Lesson,
            course__slug=self.kwargs['course_slug'],
            slug=self.kwargs['lesson_slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.object

        for assignment in lesson.assignments.all():
            assignment.user_submission = assignment.submissions.filter(
                student=self.request.user
            ).first()

        return context



from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

class LessonCompletedView(LoginRequiredMixin, View):
    def post(self, request, course_slug, lesson_slug):
        lesson = get_object_or_404(
            Lesson,
            course__slug=course_slug,
            slug=lesson_slug
        )

        if lesson.course.students.filter(id=request.user.id).exists():
            LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

        return redirect('course_detail', slug=course_slug)