"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from main import views as main_views
from catalog import views as catalog_views

from django.contrib import admin
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('signup/' , main_views.sign_up , name='signup'),
    path('logout/' , main_views.logout_ , name='logout'),
    path('profile/' , main_views.profile , name='profile'),
    path('login/' , main_views.login_view , name='login'),

    path('courses/', catalog_views.course_list, name='course_list'),
    path('course/<slug:slug>/', catalog_views.course_detail, name='course_detail'),
    path('course/<slug:slug>/enroll/', catalog_views.enroll_in_course, name='enroll_in_course'),


    path('my-courses/', catalog_views.my_courses, name='my_courses'),


    path('teacher/dashboard/', catalog_views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/course/create/', catalog_views.course_create, name='course_create'),
    path('teacher/course/<slug:slug>/edit/', catalog_views.course_update, name='course_update'),
    path('teacher/course/<slug:slug>/delete/', catalog_views.course_delete, name='course_delete'),
    path('teacher/course/<slug:course_slug>/add-lesson/', catalog_views.create_lesson, name='create_lesson'),
    path('teacher/course/<slug:course_slug>/edit-lesson/<slug:lesson_slug>/', catalog_views.update_lesson, name='update_lesson'),
    path('course/<slug:course_slug>/lesson/<slug:lesson_slug>/', catalog_views.get_lesson, name='lesson_detail'),
    path('course/<slug:course_slug>/lesson/<slug:lesson_slug>/complete/', catalog_views.lesson_completed, name='lesson_completed'),
]
