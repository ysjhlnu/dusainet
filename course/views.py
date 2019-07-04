from django.shortcuts import redirect
from django.views.generic import ListView
from django.http import HttpResponse
from django.db.models import Sum, Count

from .models import Course


# Create your views here.
class CourseListView(ListView):
    """
    教程list
    """
    template_name = 'course/course_list.html'
    context_object_name = 'courses'
    model = Course

    def get_queryset(self):
        queryset = super(CourseListView, self).get_queryset()
        queryset = queryset.annotate(likes_sum=Sum('article__likes')).annotate(articles_count=Count('article')).annotate(views_sum=Sum('article__total_views'))
        return queryset


def course_articles_list(request, course_id):
    """
    教程中course_sequence最小的博文
    """
    try:
        article = Course.objects.get(id=course_id).article.order_by('course_sequence')[0]
        return redirect(article)
    except:
        return HttpResponse('还没有文章')
