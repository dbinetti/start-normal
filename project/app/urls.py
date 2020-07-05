# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    # Public
    path('', views.index, name='index',),
    path('about', views.about, name='about',),
    path('district/<short>', views.district, name='district'),
    path('district', views.districts, name='districts'),
    path('faq', views.faq, name='faq',),
    path('goodbye', views.goodbye, name='goodbye'),
    path('morrow', views.morrow, name='morrow',),
    path('petition/<id>', views.petition, name='petition',),
    path('subscribe', views.subscribe, name='subscribe',),
    path('thomas', views.thomas, name='thomas',),
    path('videos', views.videos, name='videos',),

    # Private
    path('account', views.account, name='account',),
    path('delete', views.delete, name='delete',),
    path('signature/<id>/add', views.signature_add, name='signature-add'),
    path('signature/<id>/remove', views.signature_remove, name='signature-remove'),

    # Authentication
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),

    # Staff
    path('report', views.report, name='report',),
]
