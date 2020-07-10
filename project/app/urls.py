# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    # Root
    path('', views.index, name='index',),
    path('about', views.about, name='about',),

    # Involved
    path('involved', views.involved, name='involved'),
    path('petition/<slug>', views.petition, name='petition'),
    path('signature/<id>', views.signature, name='signature'),

    # Informed
    path('informed', views.informed, name='informed',),
    path('morrow', views.morrow, name='morrow',),
    path('thomas', views.thomas, name='thomas',),

    # Account
    path('account', views.account, name='account',),
    path('pending', views.pending, name='pending',),
    path('welcome', views.welcome, name='welcome',),
    path('delete', views.delete, name='delete',),

    # Authentication
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),

    # Admin
    path('report', views.report, name='report',),
]
