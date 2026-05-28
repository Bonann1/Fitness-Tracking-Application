from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('coach/clients/', views.CoachClientListView.as_view(), name='coach_clients'),
    path('coach/users/<int:user_id>/', views.coach_user_detail, name='coach_user_detail'),
    path('coach/users/<int:user_id>/feedback/', views.CoachFeedbackCreateView.as_view(), name='coach_feedback_create'),
    path('feedback/', views.CoachFeedbackListView.as_view(), name='feedback_list'),
]
