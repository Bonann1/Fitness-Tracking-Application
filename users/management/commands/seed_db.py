from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from workouts.models import ExerciseType, Workout, WorkoutExercise
from progress.models import ProgressEntry
from goals.models import Goal
from users.models import CoachAssignment, CoachFeedback
import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Popola il database con dati demo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Pulizia db...')
        User.objects.filter(is_superuser=False).delete()
        ExerciseType.objects.all().delete()

        self.stdout.write('Creazione utenti...')
        admin = User.objects.create_superuser('admin_demo', 'admin@demo.com', 'admin12345')
        admin.role = 'standard'
        admin.save()

        coach = User.objects.create_user('coach_demo', 'coach@demo.com', 'coach12345')
        coach.role = 'coach'
        coach.bio = 'Coach professionista con 10 anni di esperienza nel fitness.'
        coach.save()

        user1 = User.objects.create_user('user_demo', 'user@demo.com', 'user12345')
        user1.role = 'standard'
        user1.bio = 'Appassionato di fitness, obiettivo: aumentare la forza.'
        user1.save()

        user2 = User.objects.create_user('user_demo2', 'user2@demo.com', 'user12345')
        user2.role = 'standard'
        user2.bio = 'Runner amatoriale, mi alleno 4 volte a settimana.'
        user2.save()

        self.stdout.write('Creazione assegnazioni coach...')
        CoachAssignment.objects.create(coach=coach, user=user1)
        CoachAssignment.objects.create(coach=coach, user=user2)

        self.stdout.write('Creazione esercizi...')
        exercises_data = [
            ('Squat', 'strength'),
            ('Deadlift', 'strength'),
            ('Bench Press', 'strength'),
            ('Pull-up', 'strength'),
            ('Push-up', 'strength'),
            ('Rowing', 'strength'),
            ('Corsa', 'cardio'),
            ('Ciclismo', 'cardio'),
            ('Plank', 'flexibility'),
            ('Stretching', 'flexibility'),
        ]
        exercise_objs = {}
        for name, cat in exercises_data:
            exercise_objs[name] = ExerciseType.objects.create(name=name, category=cat)

        self.stdout.write('Creazione workout...')
        today = datetime.date.today()
        workout_data = [
            ('Allenamento Forza 1', [('Squat', {'sets': 3, 'reps': 10, 'weight': 80}), ('Bench Press', {'sets': 3, 'reps': 8, 'weight': 60}), ('Deadlift', {'sets': 3, 'reps': 5, 'weight': 100})]),
            ('Cardio + Core', [('Corsa', {'distance': 5.0}), ('Plank', {'sets': 3, 'reps': 60}), ('Push-up', {'sets': 3, 'reps': 15})]),
            ('Allenamento Forza 2', [('Pull-up', {'sets': 4, 'reps': 8}), ('Rowing', {'sets': 3, 'reps': 12, 'weight': 50}), ('Squat', {'sets': 4, 'reps': 8, 'weight': 85})]),
            ('Cardio Intenso', [('Ciclismo', {'distance': 20.0}), ('Corsa', {'distance': 3.0})]),
            ('Full Body', [('Squat', {'sets': 4, 'reps': 10, 'weight': 87}), ('Bench Press', {'sets': 3, 'reps': 10, 'weight': 62}), ('Pull-up', {'sets': 3, 'reps': 10}), ('Stretching', {'sets': 1, 'reps': 10})]),
        ]
        for i, (title, exs) in enumerate(workout_data):
            w = Workout.objects.create(
                user=user1,
                created_by=user1,
                title=title,
                date=today - datetime.timedelta(days=i * 3),
                duration=60 + i * 5,
                notes=f'Sessione demo {i + 1}'
            )
            for ex_name, ex_data in exs:
                WorkoutExercise.objects.create(
                    workout=w,
                    exercise=exercise_objs[ex_name],
                    **ex_data
                )

        self.stdout.write('Creazione goals...')
        goal_generic = Goal.objects.create(
            user=user1,
            title='Allenarmi 3 volte a settimana',
            description='Mantenere una routine costante di allenamento',
            goal_type='generic',
            status='active'
        )
        goal_metric = Goal.objects.create(
            user=user1,
            title='Raggiungere 100kg di squat',
            description='Progressione graduale nel Squat fino a 100kg',
            goal_type='metric',
            metric='weight',
            target_value=100.0,
            deadline=today + datetime.timedelta(days=90),
            status='active'
        )

        self.stdout.write('Creazione progress entries...')
        progress_values = [70, 75, 80, 85, 88]
        for i, val in enumerate(progress_values):
            ProgressEntry.objects.create(
                user=user1,
                goal=goal_metric,
                date=today - datetime.timedelta(days=(5 - i) * 7),
                value=val,
                notes=f'Sessione squat {i + 1}: {val}kg'
            )

        self.stdout.write('Creazione feedback coach...')
        CoachFeedback.objects.create(
            coach=coach,
            user=user1,
            message='Ottimi progressi nello squat! Stai migliorando costantemente. Continua così.'
        )
        CoachFeedback.objects.create(
            coach=coach,
            user=user1,
            message='Ricordati di scaldarti bene prima dello squat pesante. Aggiungi 10 minuti di mobilità.'
        )

        self.stdout.write(self.style.SUCCESS('Database popolato con successo!'))
        self.stdout.write('')
        self.stdout.write('Account demo:')
        self.stdout.write('  admin_demo / admin12345  (superuser)')
        self.stdout.write('  coach_demo / coach12345  (coach)')
        self.stdout.write('  user_demo  / user12345   (standard)')
        self.stdout.write('  user_demo2 / user12345   (standard)')
