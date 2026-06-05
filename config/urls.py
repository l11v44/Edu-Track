from default_pages import views as default_views
from main import views as main_views
from catalog import views as catalog_views
from assessment import views as assessment_views
from django.contrib import admin
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls), ###############
    path('', main_views.HomeView.as_view(), name='home'),   ###########
    path('signup/' , main_views.SignUpView.as_view() , name='signup'),  #############
    path('logout/', main_views.MyLogoutView.as_view(), name='logout'),   #########
    path('profile/' , main_views.ProfileView.as_view() , name='profile'),    ###########
    path('login/' , main_views.MyLoginView.as_view() , name='login'),   ###############

    path('courses/', catalog_views.CourseListView.as_view(), name='course_list'),  ###############
    path('course/<slug:slug>/', catalog_views.CourseDetailView.as_view(), name='course_detail'), #################
    path('course/<slug:slug>/enroll/', catalog_views.EnrollInCourseView.as_view(), name='enroll_in_course'),################


    path('my-courses/', catalog_views.MyCoursesView.as_view(), name='my_courses'),    #############


    path('teacher/dashboard/', catalog_views.TeacherDashboardView.as_view(), name='teacher_dashboard'),   ###############
    path('teacher/course/create/', catalog_views.CourseCreateView.as_view(), name='course_create'),  ############
    path('teacher/course/<slug:slug>/edit/', catalog_views.CourseUpdateView.as_view(), name='course_update'),   ##############
    path('teacher/course/<slug:slug>/delete/', catalog_views.CourseDeleteView.as_view(), name='course_delete'),   #################
    path('teacher/course/<slug:course_slug>/add-lesson/', catalog_views.LessonCreateView.as_view(), name='create_lesson'),   ################
    path('teacher/course/<slug:course_slug>/edit-lesson/<slug:lesson_slug>/', catalog_views.LessonUpdateView.as_view(), name='update_lesson'),  ############
    path('course/<slug:course_slug>/lesson/<slug:lesson_slug>/', catalog_views.LessonDetailView.as_view(), name='lesson_detail'),    #######################
    path('course/<slug:course_slug>/lesson/<slug:lesson_slug>/complete/', catalog_views.LessonCompletedView.as_view(), name='lesson_completed'), ##########

    path('course/<slug:course_slug>/lesson/<slug:lesson_slug>/assignment/create/', ######
         assessment_views.AssignmentCreateView.as_view(), name='create_assignment'), ####


    path('teacher/submissions/pending/',                                                         ##############
         assessment_views.TeacherPendingSubmissionsView.as_view(), name='teacher_pending_submissions'),   ###
    path('submission/<int:submission_id>/grade/',
         assessment_views.GradeSubmissionView.as_view(), name='grade_submission'),
    path('assignment/<int:assignment_id>/submit/',
         assessment_views.SubmitAssignmentView.as_view(), name='submit_assignment'),
    path('my/grades/',
         assessment_views.StudentGradesView.as_view(), name='student_grades'),
    path('grade/<int:grade_id>/',
         assessment_views.GradeDetailView.as_view(), name='grade_detail'),

    path('about/', default_views.AboutView.as_view(), name='about'),
    path('manifesto/', default_views.ManifestoView.as_view(), name='manifesto'),
    path('methodology/', default_views.MethodologyView.as_view(), name='methodology'),
    path('security/', default_views.SecurityView.as_view(), name='security'),
    path('careers/', default_views.CareersView.as_view(), name='careers'),
    path('investors/', default_views.InvestorsView.as_view(), name='investors'),
]





