from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import Workout, WorkoutExercise
from .forms import WorkoutForm, WorkoutExerciseForm
from users.models import CoachAssignment


class FriendlyPermissionDeniedMixin:
    permission_denied_message = 'Non hai i permessi per eseguire questa azione.'
    permission_denied_redirect = 'dashboard'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.permission_denied_redirect)
        return super().handle_no_permission()


class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts/workout_list.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        return Workout.objects.filter(
            user=self.request.user
        ).prefetch_related('workout_exercises__exercise')


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = 'workouts/workout_detail.html'
    context_object_name = 'workout'

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = self.object.workout_exercises.select_related('exercise').all()
        context['exercise_form'] = WorkoutExerciseForm()
        return context


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'workouts/workout_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Workout creato con successo.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('workout_detail', kwargs={'pk': self.object.pk})


class WorkoutUpdateView(LoginRequiredMixin, FriendlyPermissionDeniedMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'workouts/workout_form.html'

    def test_func(self):
        workout = self.get_object()
        user = self.request.user
        is_owner = workout.user == user
        is_assigned_coach = (
            user.role == 'coach' and
            CoachAssignment.objects.filter(coach=user, user=workout.user).exists()
        )
        return is_owner or is_assigned_coach

    def form_valid(self, form):
        form.instance.user = self.get_object().user
        messages.success(self.request, 'Workout aggiornato con successo.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('workout_detail', kwargs={'pk': self.object.pk})


class WorkoutDeleteView(LoginRequiredMixin, FriendlyPermissionDeniedMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    template_name = 'workouts/workout_confirm_delete.html'
    success_url = reverse_lazy('workout_list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Workout eliminato.')
        return super().form_valid(form)


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutExercise
    form_class = WorkoutExerciseForm
    template_name = 'workouts/exercise_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout'] = get_object_or_404(Workout, pk=self.kwargs['pk'], user=self.request.user)
        return context

    def form_valid(self, form):
        workout = get_object_or_404(Workout, pk=self.kwargs['pk'], user=self.request.user)
        form.instance.workout = workout
        messages.success(self.request, 'Esercizio aggiunto.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('workout_detail', kwargs={'pk': self.kwargs['pk']})


class ExerciseDeleteView(LoginRequiredMixin, FriendlyPermissionDeniedMixin, UserPassesTestMixin, DeleteView):
    model = WorkoutExercise
    template_name = 'workouts/exercise_confirm_delete.html'
    pk_url_kwarg = 'epk'

    def test_func(self):
        exercise = self.get_object()
        return exercise.workout.user == self.request.user

    def get_success_url(self):
        return reverse('workout_detail', kwargs={'pk': self.object.workout.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Esercizio rimosso.')
        return super().form_valid(form)
