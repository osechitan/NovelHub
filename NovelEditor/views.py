import logging
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import Novel
from .models import NovelHistory
from .forms import NovelCreateForm
from .forms import NovelUpdateForm
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


class NovelUpdateView(LoginRequiredMixin, generic.CreateView):
    model = NovelHistory
    template_name = 'novel_update.html'
    form_class = NovelUpdateForm

    def get_initial(self):
        novel = Novel.objects.filter(id=self.kwargs['pk'])
        initial = super().get_initial()
        # initial["title"] = novel[0].title
        initial["body"] = novel[0].body
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'history': NovelHistory.objects.filter(novel_id=self.kwargs['pk'])
        })
        return context

    def form_valid(self, form):

        # version = Novel.objects.filter(user=self.request.user).aggregate(latest_version=Max('version'))
        novel_history = form.save(commit=False)
        novel = Novel.objects.get(id=self.kwargs['pk'])
        novel_history.novel_id = novel
        novel_history.created_at = timezone.now()
        novel_history.updated_at = timezone.now()
        # novel.version = version['latest_version'] + 1
        novel_history.save()
        # messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('NovelHub:novel_detail', kwargs={'pk': self.kwargs['pk']})


"""
class NovelUpdateView(LoginRequiredMixin, generic.FormView):
    model = Novel
    template_name = 'novel_update.html'
    form_class = NovelUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'history': NovelHistory.objects.filter(novel_id=self.kwargs['pk'])
        })
        return context

    def get_success_url(self):
        return reverse_lazy('NovelHub:novel_detail', kwargs={'pk': self.kwargs['pk']})
"""

"""
class NovelUpdateView(LoginRequiredMixin, generic.TemplateView):
    model = Novel
    template_name = 'novel_update.html'
    form_class = NovelUpdateForm

    def get(self, request, *args, **kwargs):
        form = NovelUpdateForm(request.POST)
        form.is_valid()
        history = NovelHistory.objects.filter(novel_id=kwargs['pk'])
        return render(request, 'novel_update.html', {'form': form, 'history': history})

    def get_success_url(self):
        return reverse_lazy('NovelHub:novel_detail', kwargs={'pk': self.kwargs['pk']})
"""