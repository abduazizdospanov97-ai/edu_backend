from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def root(_request):
    return JsonResponse({
        'name': 'EduCRM API',
        'status': 'ok',
        'version': '1.0',
        'admin': '/admin/',
        'endpoints': [
            '/api/auth/',
            '/api/students/',
            '/api/groups/',
            '/api/courses/',
            '/api/rooms/',
            '/api/teachers/',
            '/api/payments/',
            '/api/attendance/',
            '/api/tests/',
            '/api/debtors/',
            '/api/dashboard/',
        ],
    })


urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),

    # API v1
    path('api/auth/',       include('apps.users.urls')),
    path('api/courses/',    include('apps.courses.urls')),
    path('api/rooms/',      include('apps.rooms.urls')),
    path('api/teachers/',   include('apps.teachers.urls')),
    path('api/groups/',     include('apps.groups.urls')),
    path('api/students/',   include('apps.students.urls')),
    path('api/payments/',   include('apps.payments.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/tests/',      include('apps.tests.urls')),
    path('api/debtors/',    include('apps.payments.debtor_urls')),
    path('api/dashboard/',  include('apps.dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
