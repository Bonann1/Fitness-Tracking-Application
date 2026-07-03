from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import CustomUser, CoachAssignment, CoachFeedback
from .forms import RegisterForm, ProfileUpdateForm, CoachFeedbackForm
from workouts.views import FriendlyPermissionDeniedMixin


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')


class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registrazione completata! Effettua il login.')
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = CoachFeedback.objects.filter(
            user=self.request.user
        ).select_related('coach')
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profilo aggiornato con successo.')
        return super().form_valid(form)


class CoachClientListView(LoginRequiredMixin, FriendlyPermissionDeniedMixin, UserPassesTestMixin, ListView):
    template_name = 'users/coach_clients.html'
    context_object_name = 'assignments'

    def test_func(self):
        return self.request.user.role == 'coach'

    def get_queryset(self):
        return CoachAssignment.objects.filter(
            coach=self.request.user
        ).select_related('user')


def coach_user_detail(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role != 'coach':
        messages.error(request, 'Accesso negato.')
        return redirect('dashboard')
    assignment = get_object_or_404(CoachAssignment, coach=request.user, user_id=user_id)
    target_user = assignment.user
    from workouts.models import Workout
    from goals.models import Goal
    from progress.models import ProgressEntry
    context = {
        'target_user': target_user,
        'workouts': Workout.objects.filter(user=target_user)[:10],
        'goals': Goal.objects.filter(user=target_user),
        'progress_entries': ProgressEntry.objects.filter(user=target_user)[:10],
        'feedbacks': CoachFeedback.objects.filter(coach=request.user, user=target_user),
    }
    return render(request, 'users/coach_user_detail.html', context)


class CoachFeedbackCreateView(LoginRequiredMixin, FriendlyPermissionDeniedMixin, UserPassesTestMixin, CreateView):
    model = CoachFeedback
    form_class = CoachFeedbackForm
    template_name = 'users/feedback_form.html'

    def test_func(self):
        return self.request.user.role == 'coach'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = get_object_or_404(
            CustomUser, pk=self.kwargs['user_id']
        )
        return context

    def form_valid(self, form):
        target_user = get_object_or_404(CustomUser, pk=self.kwargs['user_id'])
        get_object_or_404(CoachAssignment, coach=self.request.user, user=target_user)
        form.instance.coach = self.request.user
        form.instance.user = target_user
        messages.success(self.request, 'Feedback inviato con successo.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('coach_user_detail', kwargs={'user_id': self.kwargs['user_id']})


class CoachFeedbackListView(LoginRequiredMixin, ListView):
    model = CoachFeedback
    template_name = 'users/feedback_list.html'
    context_object_name = 'feedbacks'

    def get_queryset(self):
        return CoachFeedback.objects.filter(
            user=self.request.user
        ).select_related('coach')
