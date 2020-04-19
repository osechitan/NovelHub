from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic, View
from django.utils import timezone
from django.db import transaction
import logging

from .models import Novel
from .models import NovelHistory
from .forms import NovelCreateForm

logger = logging.getLogger(__name__)

REVISION_ID = 1

class TopView(generic.TemplateView):
    """
    トップ画面表示ビュー
    """

    template_name = 'top.html'



class NovelListView(LoginRequiredMixin, generic.ListView):
    """
    小説一覧表示用ビュー
    """

    model = Novel
    template_name = 'novel_list.html'

    def get_queryset(self):
        """
        小説一覧を返す関数
        """

        novels = Novel.objects.filter(user=self.request.user).order_by('-created_at')
        return novels


class NovelDetailView(LoginRequiredMixin, generic.DetailView):
    """
    小説詳細表示用ビュー
    """

    model = Novel
    template_name = 'novel_detail.html'


class NovelCreateView(LoginRequiredMixin, generic.CreateView):
    """
    小説作成用ビュー
    """

    template_name = 'novel_create.html'
    form_class = NovelCreateForm
    success_url = reverse_lazy('NovelHub:novel_list')

    def form_valid(self, form):
        """
        小説作成して履歴を作成する関数
        """

        novel = form.save(commit=False)
        novel.user = self.request.user
        novel.updated_at = timezone.now()

        #小説/履歴モデル保存時にエラーの場合はロールバックする
        with transaction.atomic():
             
            novel.save()
            # 小説モデルに紐づく履歴モデル作成
            NovelHistory().create_history_data(
                novel=novel,
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
                revision_id=REVISION_ID
            )
        
        messages.success(self.request, '作成しました。')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '作成に失敗しました。')
        return super().form_invalid(form)


class NovelUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    小説更新用ビュー
    """

    model = Novel
    template_name = 'novel_update.html'
    form_class = NovelCreateForm

    def get_context_data(self, **kwargs):
        """
        小説に紐づく履歴5件を返す関数
        """

        context = super().get_context_data(**kwargs)
        # 小説モデルに紐づく小説履歴最新5件取得
        context.update({
            'history': NovelHistory.objects.filter(novel_id=self.kwargs['pk']).all().order_by('-created_at')[:5]
        })
        return context

    def form_valid(self, form):
        """
        小説更新して履歴を作成する関数
        """
        
        # 小説モデル更新
        novel = form.save(commit=False)
        novel.updated_at = timezone.now()
        novel.revision_id += REVISION_ID

        # 小説/履歴モデル保存時にエラーの場合はロールバックする
        with transaction.atomic():
            novel.save()
            # 小説モデルに紐づく履歴モデル作成
            NovelHistory().create_history_data(
                novel=novel,
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
                revision_id=form.cleaned_data['revision_id'] + REVISION_ID
            )
        messages.success(self.request, '更新しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '更新に失敗しました。')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('NovelHub:novel_detail', kwargs={'pk': self.kwargs['pk']})


class NovelRevertView(LoginRequiredMixin, View):
    """
    履歴から戻すビュー
    """

    def post(self, request, *args, **kwargs):
        """
        履歴から戻す関数
        """

        # 履歴モデルから戻す処理
        novel = Novel().novel_revert(kwargs['pk'])
        messages.success(self.request, '過去履歴から戻しました。')
        return redirect(reverse('NovelHub:novel_detail', kwargs={'pk': novel.id}))


class NovelDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    小説削除用ビュー
    """

    model = Novel
    template_name = 'novel_delete.html'
    success_url = reverse_lazy('NovelHub:novel_list')

    def delete(self, request, *args, **kwargs):
        """
        小説削除関数
        """

        messages.success(self.request, '削除しました。')
        return super().delete(request, *args, **kwargs)