from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import ProgressEntry
from .forms import ProgressEntryForm


class ProgressListView(LoginRequiredMixin, ListView):
    model = ProgressEntry
    template_name = 'progress/progress_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return ProgressEntry.objects.filter(
            user=self.request.user
        ).select_related('goal')


class ProgressCreateView(LoginRequiredMixin, CreateView):
    model = ProgressEntry
    form_class = ProgressEntryForm
    template_name = 'progress/progress_form.html'
    success_url = reverse_lazy('progress_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Progresso registrato con successo.')
        return super().form_valid(form)


class ProgressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProgressEntry
    form_class = ProgressEntryForm
    template_name = 'progress/progress_form.html'
    success_url = reverse_lazy('progress_list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Progresso aggiornato.')
        return super().form_valid(form)


class ProgressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProgressEntry
    template_name = 'progress/progress_confirm_delete.html'
    success_url = reverse_lazy('progress_list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Voce eliminata.')
        return super().form_valid(form)
