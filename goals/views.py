import json
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import Goal
from .forms import GoalForm
from progress.models import ProgressEntry
from workouts.views import FriendlyPermissionDeniedMixin


class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'goals/goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalDetailView(LoginRequiredMixin, DetailView):
    model = Goal
    template_name = 'goals/goal_detail.html'
    context_object_name = 'goal'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = ProgressEntry.objects.filter(
            goal=self.object
        ).order_by('date')
        context['progress_entries'] = entries
        context['chart_dates'] = json.dumps([str(e.date) for e in entries])
        context['chart_values'] = json.dumps([e.value for e in entries])
        context['chart_target'] = self.object.target_value
        return context


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/goal_form.html'
    success_url = reverse_lazy('goal_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Obiettivo creato con successo.')
        return super().form_valid(form)


class GoalUpdateView(LoginRequiredMixin, FriendlyPermissionDeniedMixin, UserPassesTestMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/goal_form.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Obiettivo aggiornato.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('goal_detail', kwargs={'pk': self.object.pk})


class GoalDeleteView(LoginRequiredMixin, FriendlyPermissionDeniedMixin, UserPassesTestMixin, DeleteView):
    model = Goal
    template_name = 'goals/goal_confirm_delete.html'
    success_url = reverse_lazy('goal_list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Obiettivo eliminato.')
        return super().form_valid(form)
