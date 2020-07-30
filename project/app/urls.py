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
    path('join/<id>', views.join, name='join'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),

    # Account
    path('dashboard', views.dashboard, name='dashboard',),
    path('teacher', views.teacher, name='teacher',),
    path('homeroom/<id>', views.homeroom, name='homeroom',),
    path('homeroom/<homeroom_id>/add-student', views.add_student, name='add-student',),
    path('homeroom/<homeroom_id>/<student_id>', views.add_classmate, name='add-classmate',),
    path('addme/<id>', views.addme, name='addme',),
    path('invite/<student_id>', views.invite, name='invite',),
    path('joinhomeroom', views.join_homeroom, name='join-homeroom',),
    path('student/<id>', views.student, name='student',),
    path('parent', views.parent, name='parent',),
    path('share', views.share, name='share',),
    path('delete', views.delete, name='delete',),

    # Schools
    path('school-autocomplete', views.SchoolAutocomplete.as_view(), name='school-autocomplete',),
    path('school/add-school', views.add_school, name='add-school'),
    path('school/<slug>', views.school, name='school'),
    path('school/<slug>/add-contact', views.add_contact, name='add-contact'),
    path('school/<slug>/add-report', views.add_report, name='add-report'),
    path('search', views.search, name='search'),
    path('create-student', views.create_student, name='create-student'),
    path('delete-student/<id>', views.delete_student, name='delete-student'),

    # Informed
    path('informed', views.informed, name='informed',),
    path('morrow', views.morrow, name='morrow',),
    path('thomas', views.thomas, name='thomas',),
]
