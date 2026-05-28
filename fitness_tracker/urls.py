from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard'), name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', include('users.urls')),
    path('', include('workouts.urls')),
    path('', include('progress.urls')),
    path('', include('goals.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
