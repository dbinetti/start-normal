# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    # Public
    path('', views.index, name='index',),
    path('morrow', views.morrow, name='morrow',),
    path('about', views.about, name='about',),
    path('videos', views.videos, name='videos',),
    path('thomas', views.thomas, name='thomas',),
    path('district/<short>/', views.district, name='district'),
    path('district/', views.districts, name='districts'),
    # path('petition', views.petition, name='petition',),
    # path('signatures', views.signatures, name='signatures',),
    path('subscribe', views.subscribe, name='subscribe',),
    path('faq', views.faq, name='faq',),

    # Authentication
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),
    path('goodbye', views.goodbye, name='goodbye'),

    # Private
    # path('sign', views.sign, name='sign',),
    path('account', views.account, name='account',),
    # path('signature', views.signature, name='signature',),
    path('delete', views.delete, name='delete',),
    # path('thanks', views.thanks, name='thanks',),

    # Staff
    path('report', views.report, name='report',),
    path('notes', views.notes, name='notes',),
]
