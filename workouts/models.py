from django.db import models
from django.conf import settings


class ExerciseType(models.Model):
    CATEGORY_CHOICES = [
        ('strength', 'Forza'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flessibilità'),
        ('other', 'Altro'),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Workout(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workouts'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_workouts'
    )
    title = models.CharField(max_length=200)
    date = models.DateField()
    duration = models.IntegerField(help_text='Durata in minuti')
    notes = models.TextField(blank=True)
    exercises = models.ManyToManyField(
        ExerciseType,
        through='WorkoutExercise',
        blank=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date})"


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='workout_exercises'
    )
    exercise = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, help_text='Peso in kg')
    distance = models.FloatField(null=True, blank=True, help_text='Distanza in km')

    def __str__(self):
        return f"{self.exercise.name} in {self.workout.title}"
