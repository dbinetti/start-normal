# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    path('', views.index, name='index',),
    path('letter', views.letter, name='letter',),
    # path('thanks', views.thanks, name='thanks',),
    # path('data', views.data, name='data',),
    # path('morrow', views.morrow, name='morrow',),
    # path('about', views.about, name='about',),
    # path('harm', views.about, name='harm',),
    # path('unsustainable', views.unsustainable, name='unsustainable',),
    # path('unrealistic', views.unrealistic, name='unrealistic',),
    # path('framework', views.framework, name='framework',),
    # path('transcript', views.transcript, name='transcript',),
    path('report', views.report, name='report',),
    path('notes', views.notes, name='notes',),
]
