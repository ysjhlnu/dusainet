from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from .models import ArticlesPost

from uuid import uuid1
import time


def create_author():
    username = str(uuid1())
    author = User.objects.create_user(username, password='test_password')
    return author


class ArticlesPostModelTests(TestCase):
    """文章模型测试"""

    def test_create(self):
        """文章是否能正常创建"""
        article = ArticlesPost(title='article_create_title', body='article_create_body', author=create_author())
        article.save()
        article_in_db = ArticlesPost.objects.get(title='article_create_title')
        self.assertEqual(article_in_db.body, 'article_create_body')

    def test_increase_views(self):
        """增加阅读量"""
        article = ArticlesPost(title='test_increase_views', body='test_increase_views', author=create_author())
        article.save()
        time.sleep(0.2)
        article.increase_views()
        self.assertIs(article.total_views, 1)
        self.assertIs(article.updated - article.created < timezone.timedelta(seconds=0.1), True)

    def test_updated_field_change(self):
        """更新文章后updated字段是否更新"""
        article = ArticlesPost(title='test_updated_field_change', body='test_updated_field_change',
                               author=create_author())
        article.save()
        time.sleep(0.1)
        article.save()
        self.assertIsNot(article.created, article.updated)


class ArticlesPostViewTests(TestCase):
    """文章视图测试"""

    def test_get_article_detail(self):
        """获取文章详情"""
        article = ArticlesPost(title='get_article_detail_title', body='get_article_detail_body', author=create_author())
        article.save()
        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)
        self.assertContains(response, article.body)

    def test_increase_views(self):
        """get文章详情, 浏览量 +1 并且 updated字段不更新"""
        article = ArticlesPost(title='increase_views_title', body='increase_views_body', author=create_author())
        article.save()
        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)
        response_article_total_views = response.context.get('article').total_views
        self.assertIs(response_article_total_views, 1)
        self.assertIs(article.updated - article.created < timezone.timedelta(seconds=0.1), True)
