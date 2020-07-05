# Django
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain",
    )),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
