from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from django.utils import timezone
import logging

from .models import Novel
from .models import NovelHistory
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


class NovelListView(LoginRequiredMixin, generic.ListView):
    model = Novel
    template_name = 'novel_list.html'

    def get_queryset(self):
        novels = Novel.objects.filter(user=self.request.user).order_by('-created_at')
        return novels


class NovelDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'novel_detail.html'

    def get_queryset(self):
        # 最新5件取得
        novels = Novel.objects.filter(user=self.request.user).order_by('-created_at')
        return novels


class NovelCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'novel_create.html'
    form_class = NovelCreateForm
    success_url = reverse_lazy('NovelHub:novel_list')

    def form_valid(self, form):
        novel = form.save(commit=False)
        novel.user = self.request.user
        novel.updated_at = timezone.now()
        novel.save()

        # 小説モデルに紐づく履歴モデル作成
        NovelHistory().create_history_data(novel=novel, title=form.cleaned_data['title'], body=form.cleaned_data['body'])
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class NovelUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Novel
    template_name = 'novel_update.html'
    form_class = NovelCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 小説モデルに紐づく小説履歴最新5件取得
        context.update({
            'history': NovelHistory.objects.filter(novel_id=self.kwargs['pk']).all().order_by('-created_at')[:5]
        })
        return context

    def form_valid(self, form):
        # 小説モデル更新
        novel = form.save(commit=False)
        novel.updated_at = timezone.now()
        novel.save()

        # 小説モデルに紐づく履歴モデル作成
        NovelHistory().create_history_data(
            novel=novel,
            title=form.cleaned_data['title'],
            body=form.cleaned_data['body']
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('NovelHub:novel_detail', kwargs={'pk': self.kwargs['pk']})


class NovelRevertView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        # 履歴モデルから戻す処理
        novel = Novel().novel_revert(kwargs['pk'])
        return redirect(reverse('NovelHub:novel_detail', kwargs={'pk': novel.id}))


class NovelDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Novel
    template_name = 'novel_delete.html'
    success_url = reverse_lazy('NovelHub:novel_list')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)