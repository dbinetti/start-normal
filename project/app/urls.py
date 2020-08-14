# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    # Root
    path('', views.index, name='index',),
    path('about', views.about, name='about',),
    path('faq', views.faq, name='faq',),
    path('team', views.team, name='team',),
    path('privacy', views.privacy, name='privacy',),
    path('robots.txt', views.robots, name='robots',),
    path('sitemap.txt', views.sitemap, name='sitemap',),

    # Authentication
    path('login', views.login, name='login'),
    path('signup/<kind>', views.signup, name='signup'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),

    # Dashboard
    path('dashboard', views.dashboard, name='dashboard',),
    path('dashboard/delete', views.delete_user, name='delete-user',),

    # Student
    path('student/create', views.create_student, name='create-student'),
    path('student/<student_id>', views.student, name='student',),
    path('student/<student_id>/delete', views.delete_student, name='delete-student'),

    # Teacher
    path('teacher', views.teacher, name='teacher',),

    # Parent Onboarding
    path('parent', views.parent, name='parent',),
    path('parent-edit', views.parent_edit, name='parent-edit',),
    path('student-parent', views.add_student_parent, name='add-student-parent',),
    path('homeroom/create-homerooms', views.create_homerooms, name='create-homerooms'),

    # Homeroom
    path('homeroom/search', views.homeroom_search, name='homeroom-search',),
    path('homeroom/create', views.create_homeroom, name='create-homeroom'),
    path('homeroom/<homeroom_id>', views.homeroom, name='homeroom',),
    path('homeroom/<homeroom_id>/delete', views.delete_homeroom, name='delete-homeroom',),
    path('homeroom/connect/<student_id>', views.connect_homeroom, name='connect-homeroom'),

    path('homerooms', views.homerooms, name='homerooms',),

    # Ask
    path('ask/add/<homeroom_id>', views.add_ask, name='add-ask',),
    path('ask/<homeroom_id>/<student_id>', views.ask, name='ask',),
    path('ask-form/<homeroom_id>', views.ask_form, name='ask-form',),
    path('ask-user/<homeroom_id>', views.ask_user, name='ask-user',),



    # Schools
    path('school/search', views.search_schools, name='school-search'),
    path('school/<slug>', views.school, name='school'),
    path('school-autocomplete', views.SchoolAutocomplete.as_view(), name='school-autocomplete',),
]
