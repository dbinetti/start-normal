# Django
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('sentry-debug/', trigger_error),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
