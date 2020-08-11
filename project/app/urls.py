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
    # path('share', views.share, name='share',),
    path('delete', views.delete, name='delete',),

    # Parent
    path('parent', views.parent, name='parent',),
    path('parent2', views.parent_two, name='parent-two',),
    path('student-parent', views.add_student_parent, name='add-student-parent',),
    path('ask-form/<homeroom_id>', views.ask_form, name='ask-form',),
    path('homeroom-intro', views.parent_homeroom_intro, name='parent-homeroom-intro',),
    path('homerooms', views.homerooms, name='homerooms',),
    path('student/create', views.create_student, name='create-student'),
    path('student/<student_id>', views.student, name='student',),
    path('student/<student_id>/delete', views.delete_student, name='delete-student'),

    # Teacher
    path('teacher', views.teacher, name='teacher',),

    # Homeroom
    path('homeroom/connect/<student_id>', views.connect_homeroom, name='connect-homeroom'),
    path('homeroom/create/<student_id>', views.create_homeroom, name='create-homeroom'),
    path('homeroom/<homeroom_id>', views.homeroom, name='homeroom',),
    path('homeroom/<homeroom_id>/invite', views.homeroom_invite, name='homeroom-invite',),

    # Classmate
    path('classmate/<classmate_id>', views.classmate, name='classmate',),
    path('invite/create/<homeroom_id>', views.create_invite, name='create-invite',),
    path('ask/<homeroom_id>/<student_id>', views.ask, name='ask',),
    path('invite/<invite_id>', views.invite, name='invite',),
    path('accept/<homeroom_id>', views.accept, name='accept',),

    path('homeroom/<homeroom_id>/add/<student_id>', views.add_homeroom_student, name='add-homeroom-student',),
    path('homeroom/<homeroom_id>/remove/<student_id>', views.remove_homeroom_student, name='remove-homeroom-student',),

    # Schools
    path('search', views.search, name='search'),
    path('school/add-school', views.add_school, name='add-school'),
    path('school/<slug>', views.school, name='school'),
    path('school-autocomplete', views.SchoolAutocomplete.as_view(), name='school-autocomplete',),
]
