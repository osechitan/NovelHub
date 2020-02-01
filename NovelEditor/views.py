import logging
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import Novel
from .forms import NovelCreateForm

logger = logging.getLogger(__name__)


class TopView(generic.TemplateView):
    template_name = 'top.html'


class HomeView(LoginRequiredMixin, generic.ListView):
    model = Novel
    template_name = 'home.html'

    def get_queryset(self):
        novels = Novel.objects.filter(user=self.request.user).order_by('-created_at')
        return novels


class NovelCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'diary_create.html'
    form_class = NovelCreateForm
    # success_url = reverse_lazy('diary:diary_list')
