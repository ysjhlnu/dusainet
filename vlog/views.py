from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from .models import Vlog

from comments.models import VlogComment
from comments.forms import VlogCommentForm
from utils.utils import PaginatorMixin

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin


# Create your views here.

class VlogListView(PaginatorMixin, ListView):
    """
    vlog列表
    """
    # paginate_by = 1

    model = Vlog
    context_object_name = 'articles'
    template_name = 'vlog/list.html'


class VlogDetailView(DetailView):
    """
    vlog单篇
    """
    model = Vlog
    context_object_name = 'article'
    template_name = 'vlog/detail.html'

    def get_context_data(self, **kwargs):
        context = super(VlogDetailView, self).get_context_data(**kwargs)
        self.object.increase_views()

        comment_form = VlogCommentForm()
        extra_data = {
            'comment_form': comment_form,
            # 生成树形评论
            'comments': VlogComment.objects.filter(article_id=self.object.id),
        }
        context.update(extra_data)
        return context
