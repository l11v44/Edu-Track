from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalog.views import TeacherRequiredMixin
from catalog.models import Lesson
from .models import Submission
from .forms import *


from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse

class AssignmentCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assessment/assignment_form.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        self.lesson = self.get_lesson()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.lesson = self.get_lesson()
        return super().post(request, *args, **kwargs)

    def get_lesson(self):
        return get_object_or_404(
            Lesson,
            slug=self.kwargs['lesson_slug'],
            course__slug=self.kwargs['course_slug'],
            course__author=self.request.user
        )

    def form_valid(self, form):
        form.instance.lesson = self.lesson
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = self.lesson
        return context

    def get_success_url(self):
        return reverse('lesson_detail', kwargs={
            'course_slug': self.kwargs['course_slug'],
            'lesson_slug': self.kwargs['lesson_slug']
        })



from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class TeacherPendingSubmissionsView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Submission
    template_name = 'assessment/teacher_pending_submissions.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        return Submission.objects.filter(
            assignment__lesson__course__author=self.request.user,
            status='Pending'
        )


from django.views.generic import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

class GradeSubmissionView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'assessment/grade_form.html'
    success_url = reverse_lazy('teacher_pending_submissions')

    def get(self, request, *args, **kwargs):
        self.object = None
        self.submission = self.get_submission()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.submission = self.get_submission()
        return super().post(request, *args, **kwargs)

    def get_submission(self):
        return get_object_or_404(
            Submission,
            id=self.kwargs['submission_id'],
            assignment__lesson__course__author=self.request.user
        )

    def form_valid(self, form):
        form.instance.submission = self.submission
        form.instance.teacher = self.request.user
        response = super().form_valid(form)
        self.submission.status = 'Graded'
        self.submission.save()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission'] = self.submission
        return context


from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied


class SubmitAssignmentView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'assessment/submit_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.assignment = get_object_or_404(Assignment, id=self.kwargs['assignment_id'])
        if Submission.objects.filter(student=request.user, assignment=self.assignment).exists():
            return self.redirect_to_lesson()
        if not self.assignment.lesson.course.students.filter(id=request.user.id).exists():
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.assignment = self.assignment
        form.instance.student = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.redirect_to_lesson().url

    def redirect_to_lesson(self):
        return redirect('lesson_detail',
                        course_slug=self.assignment.lesson.course.slug,
                        lesson_slug=self.assignment.lesson.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment'] = self.assignment
        return context

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class StudentGradesView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'assessment/student_grades.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return Grade.objects.filter(submission__student=self.request.user)

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

class GradeDetailView(LoginRequiredMixin, DetailView):
    model = Grade
    template_name = 'assessment/grade_detail.html'
    context_object_name = 'grade'

    def get_object(self, queryset=None):
        grade = get_object_or_404(Grade, id=self.kwargs['grade_id'])
        if grade.submission.student != self.request.user:
            raise PermissionDenied
        return grade
