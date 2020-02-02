import logging
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import Novel
from .forms import NovelCreateForm
from django.utils import timezone
from django.db.models import Max

logger = logging.getLogger(__name__)


class TopView(generic.TemplateView):
    template_name = 'top.html'


class HomeView(LoginRequiredMixin, generic.ListView):
    model = Novel
    template_name = 'home.html'

    def get_queryset(self):
        novels = Novel.objects.filter(user=self.request.user).order_by('-created_at')
        return novels


class NovelListView(LoginRequiredMixin, generic.ListView):
    model = Novel
    template_name = 'novel_list.html'

    def get_queryset(self):
        novels = Novel.objects.filter(user=self.request.user).order_by('-created_at')
        return novels


class NovelDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'novel_detail.html'

    def get_queryset(self):
        # versionの最新5件取得
        version = Novel.objects.filter(user=self.request.user).order_by('-version')
        novels = Novel.objects.filter(user=self.request.user).order_by('-created_at')
        return novels


class NovelCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'novel_create.html'
    form_class = NovelCreateForm
    success_url = reverse_lazy('NovelHub:novel_list')

    def form_valid(self, form):

        version = Novel.objects.filter(user=self.request.user).aggregate(latest_version=Max('version'))
        novel = form.save(commit=False)
        novel.user = self.request.user
        novel.updated_at = timezone.now()
        # novel.version = version['latest_version'] + 1
        novel.save()
        # messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)


class NovelUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Novel
    template_name = 'novel_update.html'
    form_class = NovelCreateForm

    def get_success_url(self):
        return reverse_lazy('NovelHub:novel_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        # messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)