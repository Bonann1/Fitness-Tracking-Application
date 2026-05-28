from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from workouts.models import Workout
from goals.models import Goal
from progress.models import ProgressEntry
from users.models import CoachAssignment, CoachFeedback


@login_required
def dashboard_view(request):
    if request.user.role == 'coach':
        context = {
            'assigned_users': CoachAssignment.objects.filter(
                coach=request.user
            ).select_related('user'),
            'recent_feedbacks': CoachFeedback.objects.filter(
                coach=request.user
            ).order_by('-date')[:5],
        }
        return render(request, 'dashboard/dashboard_coach.html', context)
    else:
        recent_workouts = Workout.objects.filter(user=request.user)[:5]
        active_goals = Goal.objects.filter(user=request.user, status='active')
        recent_progress = ProgressEntry.objects.filter(user=request.user)[:5]

        # Weekly workout data for chart
        from datetime import date, timedelta
        import json
        today = date.today()
        weeks = []
        week_counts = []
        for i in range(7, -1, -1):
            week_start = today - timedelta(days=today.weekday() + 7 * i)
            week_end = week_start + timedelta(days=6)
            count = Workout.objects.filter(
                user=request.user,
                date__gte=week_start,
                date__lte=week_end
            ).count()
            weeks.append(f"W{week_start.strftime('%d/%m')}")
            week_counts.append(count)

        context = {
            'recent_workouts': recent_workouts,
            'active_goals': active_goals,
            'recent_progress': recent_progress,
            'chart_weeks': json.dumps(weeks),
            'chart_counts': json.dumps(week_counts),
        }
        return render(request, 'dashboard/dashboard_user.html', context)
