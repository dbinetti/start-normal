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
    path('account', views.account, name='account',),
    path('pending', views.pending, name='pending',),
    path('teacher', views.teacher, name='teacher',),
    path('create-teacher', views.create_teacher, name='create-teacher',),
    path('create-homeroom/<student_id>', views.create_homeroom, name='create-homeroom',),
    path('create-parent', views.create_parent, name='create-parent',),
    path('homeroom/<id>', views.homeroom, name='homeroom',),
    path('parent', views.parent, name='parent',),
    path('create-parent', views.create_parent, name='create-parent',),
    path('share', views.share, name='share',),
    path('delete', views.delete, name='delete',),

    # Schools
    path('school-autocomplete', views.SchoolAutocomplete.as_view(), name='school-autocomplete',),
    path('school/add-school', views.add_school, name='add-school'),
    path('school/<slug>', views.school, name='school'),
    path('school/<slug>/add-contact', views.add_contact, name='add-contact'),
    path('school/<slug>/add-report', views.add_report, name='add-report'),
    path('search', views.search, name='search'),

    # Informed
    path('informed', views.informed, name='informed',),
    path('morrow', views.morrow, name='morrow',),
    path('thomas', views.thomas, name='thomas',),
]
