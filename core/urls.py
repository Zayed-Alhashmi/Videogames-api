from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Video Games Library API",
        default_version='v1',
        description="A RESTful web service providing access to a database of over 16,000 video games. Supports full CRUD operations, advanced filtering by genre, platform, critic score and release year, personalised game recommendations, and database statistics. Built using Django REST Framework with SQLite.",
        contact=openapi.Contact(email="sc22zkom@leeds.ac.uk"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='frontend.html'), name='frontend'),
    path('admin/', admin.site.urls),
    path('api/', include('games.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
