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
    path('delete', views.delete, name='delete',),
    path('account', views.account, name='account',),
    path('account/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
