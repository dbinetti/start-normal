# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    # Root
    path('', views.index, name='index',),
    path('about', views.about, name='about',),
    path('faq', views.faq, name='faq',),

    # Involved
    path('involved', views.involved, name='involved'),
    path('school/<slug>', views.school, name='school'),
    # path('district/<slug>', views.district, name='district'),
    # path('petition/<id>', views.petition, name='petition',),
    # path('signature/<id>', views.signature, name='signature'),
    # path('signature/<id>/add', views.signature_add, name='signature-add'),
    # path('signature/<id>/remove', views.signature_remove, name='signature-remove'),

    # Informed
    path('informed', views.informed, name='informed',),
    path('morrow', views.morrow, name='morrow',),
    path('thomas', views.thomas, name='thomas',),

    # Account
    path('account', views.account, name='account',),
    path('delete', views.delete, name='delete',),
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),

    # Admin
    path('report', views.report, name='report',),
]
