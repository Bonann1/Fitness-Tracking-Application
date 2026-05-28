from django.urls import path
from . import views

urlpatterns = [
    path('progress/', views.ProgressListView.as_view(), name='progress_list'),
    path('progress/add/', views.ProgressCreateView.as_view(), name='progress_add'),
    path('progress/<int:pk>/edit/', views.ProgressUpdateView.as_view(), name='progress_edit'),
    path('progress/<int:pk>/delete/', views.ProgressDeleteView.as_view(), name='progress_delete'),
]
