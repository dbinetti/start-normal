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

    # Involved
    # path('involved', views.involved, name='involved'),

    path('school/<slug>', views.school, name='school'),
    path('school', views.schools, name='schools'),

    path('district/<slug>', views.district, name='district'),
    path('district/<slug>/report', views.district_report, name='district-report'),
    # path('district/<slug>/contact', views.district_contact, name='district-contact'),
    path('district', views.districts, name='districts'),

    # Informed
    path('informed', views.informed, name='informed',),
    path('morrow', views.morrow, name='morrow',),
    path('thomas', views.thomas, name='thomas',),

    # Account
    path('account', views.account, name='account',),
    path('pending', views.pending, name='pending',),
    path('delete', views.delete, name='delete',),
    path('share', views.share, name='share',),
    path('split', views.split, name='split',),
    path('welcome-teacher', views.welcome_teacher, name='welcome-teacher',),
    path('welcome-parent', views.welcome_parent, name='welcome-parent',),

    # Authentication
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),

    # Autocomplete
    path('school-search', views.SchoolAutocomplete.as_view(), name='school-search',),

    # Admin
    # path('report', views.report, name='report',),
]
