from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import ArticlesPost, ArticlesColumn
from .forms import ArticleCreateForm
from course.models import Course
from comments.forms import CommentForm
from utils.utils import PaginatorMixin

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

import markdown

from dusainet2.settings import LOGGING
import logging

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('django.request')


class ArticleMixin(PaginatorMixin):
    """
    文章Mixin
    """
    model = ArticlesPost
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        columns = ArticlesColumn.objects.all()
        data = {
            'columns': columns
        }
        context.update(data)
        return context


# 文章列表
class ArticlePostView(ArticleMixin, ListView):
    template_name = 'article/article_list.html'

    def dispatch(self, request, *args, **kwargs):
        """init"""
        column_id_temp = self.request.GET.get('column_id')
        if column_id_temp and column_id_temp.isdigit():
            self.column_id = column_id_temp
        else:
            self.column_id = None
        self.order = self.request.GET.get('order')
        self.tag = self.request.GET.get('tag')
        return super(ArticlePostView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        获取模型数组
        :return: queryset
        """
        queryset = super(ArticlePostView, self).get_queryset()
        if self.column_id:
            queryset = queryset.filter(column=self.column_id)
        if self.order == 'total_views':
            queryset = queryset.order_by('-total_views')
        if self.tag:
            try:
                queryset = queryset.filter(tags__name__in=[self.tag])
            except:
                logger.error('ArticlePostView get_queryset get_tag went wrong!')
        return queryset

    def get_context_data(self, **kwargs):
        """
        获取上下文
        :return: context
        """
        context = super(ArticlePostView, self).get_context_data(**kwargs)
        # 更新栏目信息
        if self.column_id:
            c_data = {
                'column_id': int(self.column_id),
            }
            context.update(c_data)
        # 更新排序信息
        if self.order:
            o_data = {
                'order': self.order
            }
            context.update(o_data)
        # 更新标签信息
        if self.tag:
            t_data = {
                'tag': self.tag
            }
            context.update(t_data)
        return context


def article_detail(request, article_id):
    """
    文章详情的view
    :param article_id: 文章的id
    """
    article = get_object_or_404(ArticlesPost, id=article_id)
    try:
        article.increase_views()
    except:
        logger.error('article increase views went wrong!')

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 传递给模板文章类型，用于评论表单区分
    article_type = 'article'
    comment_form = CommentForm()

    # 根据教程序号，取出教程中前一条和后一条文章
    if article.course:
        next_article = ArticlesPost.objects.filter(
            course_sequence__gt=article.course_sequence,
            course=article.course,
        ).order_by('course_sequence')

        pre_article = ArticlesPost.objects.filter(
            course_sequence__lt=article.course_sequence,
            course=article.course
        ).order_by('-course_sequence')

        if pre_article.count() > 0:
            pre_article = pre_article[0]
        else:
            pre_article = None

        if next_article.count() > 0:
            next_article = next_article[0]
        else:
            next_article = None

        course_articles = article.course.article.all().order_by('course_sequence')

        context = {'article': article,
                   'comment_form': comment_form,
                   # 生成树形评论
                   'comments': article.comments.all(),
                   'course_articles': course_articles,
                   'pre_article': pre_article,
                   'next_article': next_article,
                   'article_type': article_type,
                   'toc': md.toc,
                   }

        return render(request, 'course/article_detail.html', context=context)
    # 文章不属于任何教程
    else:
        context = {'article': article,
                   'comment_form': comment_form,
                   # 生成树形评论
                   'comments': article.comments.all(),
                   'article_type': article_type,
                   'toc': md.toc,
                   }
        return render(request, 'article/article_detail.html', context=context)


# 发表文章
class ArticleCreateView(LoginRequiredMixin,
                        StaffuserRequiredMixin,
                        ArticleMixin,
                        CreateView):
    fields = [
        'title',
        'column',
        'tags',
        'body',
        'url',
        'course',
        'course_sequence',
    ]

    login_url = "/"
    template_name = 'article/article_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all()
        data = {
            'courses': courses
        }
        context.update(data)
        return context

    def post(self, request, *args, **kwargs):
        forms = ArticleCreateForm(data=request.POST)
        if forms.is_valid():
            new_article = forms.save(commit=False)
            new_article.author = self.request.user
            new_article.save()

            # Without this next line the tags won't be saved.
            forms.save_m2m()

            return redirect("article:article_list")
        return self.render_to_response({"forms": forms})


class ArticleUpdateView(LoginRequiredMixin,
                        StaffuserRequiredMixin,
                        View):
    """更新文章"""
    login_url = "/"

    def dispatch(self, request, *args, **kwargs):
        """init"""
        self.article = get_object_or_404(ArticlesPost, pk=kwargs.get('article_id'))
        return super(ArticleUpdateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = {
            'article': self.article,
            'columns': ArticlesColumn.objects.all(),
            'courses': Course.objects.all(),
            'tags': ','.join([x for x in self.article.tags.names()])
        }
        return render(request, 'article/article_update.html', context=context)

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        self.article.title = post_data.get('title')
        self.article.course_title = post_data.get('course_title')
        self.article.column = get_object_or_404(ArticlesColumn, pk=post_data.get('column')) if post_data.get('column') else None
        self.article.course = get_object_or_404(Course, pk=post_data.get('course')) if post_data.get('course') else None
        if self.article.course:
            self.article.course_sequence = post_data.get('course_sequence') if post_data.get('course_sequence') else 9000
        self.article.tags.set(*post_data.get('tags').split(','), clear=True)
        self.article.body = post_data.get('body')
        self.article.save()
        return redirect(self.article)
