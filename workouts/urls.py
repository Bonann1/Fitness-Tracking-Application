from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workouts/create/', views.WorkoutCreateView.as_view(), name='workout_create'),
    path('workouts/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('workouts/<int:pk>/edit/', views.WorkoutUpdateView.as_view(), name='workout_edit'),
    path('workouts/<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='workout_delete'),
    path('workouts/<int:pk>/exercise/add/', views.ExerciseCreateView.as_view(), name='exercise_add'),
    path('workouts/<int:pk>/exercise/<int:epk>/delete/', views.ExerciseDeleteView.as_view(), name='exercise_delete'),
]
