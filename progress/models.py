from django.db import models
from django.conf import settings


class ProgressEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_entries'
    )
    goal = models.ForeignKey(
        'goals.Goal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='progress_entries'
    )
    date = models.DateField()
    value = models.FloatField(
        help_text='Valore numerico (es. peso in kg, distanza in km, numero reps)'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} — {self.value} ({self.date})"
