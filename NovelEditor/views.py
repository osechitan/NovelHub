from django.shortcuts import render
from django.views import View
from django.views import generic


class HomeView(generic.TemplateView):

    template_name = 'home.html'


class TopView(generic.TemplateView):
    template_name = 'top.html'



"""
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'message': 'テスト',
        }
        return render(request, 'home.html', context)


# home = HomeView.as_view()
"""