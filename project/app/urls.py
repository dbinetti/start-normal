# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    path('', views.index, name='index',),
    path('letter', views.letter, name='letter',),
    path('thanks', views.thanks, name='thanks',),
    path('learn', views.learn, name='learn',),
    path('about', views.about, name='about',),
    path('report', views.report, name='report',),
    path('videos', views.videos, name='videos',),
    path('notes', views.notes, name='notes',),
    path('thomas', views.thomas, name='thomas',),
    path('delete', views.delete, name='delete',),
    path('account', views.account, name='account',),
    path('morrow', views.morrow, name='morrow',),
    path('sign', views.sign, name='sign',),
    path('signup', views.signup, name='signup',),
    path('petition', views.petition, name='petition',),
    path('signatures', views.signatures, name='signatures',),

    path('account/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('district/<short>/', views.district, name='district'),
    path('district/', views.districts, name='districts'),
]
