from django.contrib import admin
from .models import ExerciseType, Workout, WorkoutExercise


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 0


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'duration')
    list_filter = ('date',)
    inlines = [WorkoutExerciseInline]
