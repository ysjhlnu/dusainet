from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Comment
from .forms import CommentForm
from article.models import ArticlesPost

from uuid import uuid1
import time


def create_author():
    username = str(uuid1())
    author = User.objects.create_user(username, password='test_password')
    return author


def create_article():
    title = str(uuid1())
    body = str(uuid1())
    article = ArticlesPost(title=title, body=body, author=create_author())
    return article


class CommentModelTests(TestCase):
    """测试Comment Model"""
    def test_create_comment(self):
        article = create_article()
        comment = Comment(content_object=article, user=create_author(), body='test_create_comment', object_id=1)
        comment.save()
