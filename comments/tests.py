from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from article.models import ArticlesPost
from . import views

from uuid import uuid1


def create_author():
    username = str(uuid1())
    author = User.objects.create_user(username, password='test_password')
    return author


def create_article():
    title = str(uuid1())
    body = str(uuid1())
    article = ArticlesPost(title=title, body=body, author=create_author())
    return article


class CommentViewTests(TestCase):
    """测试Comment View"""

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = create_author()

    def test_create_comment(self):
        # 测试创建 comment
        article = ArticlesPost(
            title='test_create_comment',
            body='test_create_comment',
            author=create_author()
        )
        article.save()
        kwargs = {
            'article_id': article.id
        }
        url = reverse('comments:post_comment', kwargs=kwargs)
        body = str(uuid1())
        data = {
            'body': body,
            'article_type': 'article'
        }
        request = self.request_factory.post(url, data)
        request.user = self.user
        response = views.CommentCreateView.as_view()(request, **kwargs)
        self.assertEqual(article.comments.all()[0].body, body)
