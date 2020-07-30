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

    # Account
    path('dashboard', views.dashboard, name='dashboard',),
    path('share', views.share, name='share',),
    path('delete', views.delete, name='delete',),

    # Parent
    path('parent', views.parent, name='parent',),
    path('student/<student_id>', views.student, name='student',),
    path('create-student', views.create_student, name='create-student'),
    path('delete-student/<student_id>', views.delete_student, name='delete-student'),

    # Teacher
    path('teacher', views.teacher, name='teacher',),

    # Homeroom
    path('homeroom/<homeroom_id>/join', views.join, name='join'),
    path('homeroom/connect/<student_id>', views.connect_homeroom, name='connect-homeroom'),
    path('homeroom/create/<student_id>', views.create_homeroom, name='create-homeroom'),
    path('homeroom/<homeroom_id>', views.homeroom, name='homeroom',),
    path('homeroom/<homeroom_id>/<student_id>', views.add_classmate_from_student, name='add-classmate-from-student',),
    path('joinhomeroom', views.join_homeroom, name='join-homeroom',),

    # Schools
    path('search', views.search, name='search'),
    path('school/add-school', views.add_school, name='add-school'),
    path('school/<slug>', views.school, name='school'),
    path('school-autocomplete', views.SchoolAutocomplete.as_view(), name='school-autocomplete',),
]
