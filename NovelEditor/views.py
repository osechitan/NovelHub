import logging
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
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
        # versionの最新5件取得
        version = Novel.objects.filter(user=self.request.user).order_by('-version')
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

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class NovelUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Novel
    template_name = 'novel_update.html'
    form_class = NovelCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'history': NovelHistory.objects.filter(novel_id=self.kwargs['pk']).all()[:5]
        })
        return context

    def form_valid(self, form):

        novel = Novel.objects.get(id=self.kwargs['pk'])
        novel_history = NovelHistory()
        novel_history.novel_id = novel
        novel_history.title = form.cleaned_data['title']
        novel_history.body = form.cleaned_data['body']

        novel_history.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('NovelHub:novel_detail', kwargs={'pk': self.kwargs['pk']})
