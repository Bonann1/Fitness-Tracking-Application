from django.db import models
from django.conf import settings


class Goal(models.Model):
    GOAL_TYPES = [('generic', 'Generico'), ('metric', 'A Metrica')]
    METRICS = [
        ('weight', 'Peso (kg)'),
        ('distance', 'Distanza (km)'),
        ('reps', 'Ripetizioni'),
    ]
    STATUS = [
        ('active', 'Attivo'),
        ('completed', 'Completato'),
        ('abandoned', 'Abbandonato'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES, default='generic')
    metric = models.CharField(max_length=20, choices=METRICS, null=True, blank=True)
    target_value = models.FloatField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
