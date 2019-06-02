from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from article.views import ArticlePostView
from article.feeds import ArticlesPostRssFeed, ArticlesPostColumnRssFeed

import notifications.urls

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    path('admin/', admin.site.urls),
    url(r'^$', ArticlePostView.as_view(), name='home'),
    path('admiration/', TemplateView.as_view(template_name='utils/admiration.html'), name='admiration'),

    path('userinfo/', include('userinfo.urls', namespace='userinfo')),

    path('article/', include('article.urls', namespace='article')),
    url(r'comments/', include('comments.urls', namespace='comments')),
    path('album/', include('album.urls', namespace='album')),
    path('course/', include('course.urls', namespace='course')),

    path('book/', include('readbook.urls', namespace='readbook')),

    path('imagesource/', include('imagesource.urls', namespace='imagesource')),

    path('vlog/', include('vlog.urls', namespace='vlog')),

    path('aboutme/', include('aboutme.urls', namespace='aboutme')),

    path('my-notifications/', include('mynotifications.urls', namespace='my_notifications')),

    # RSS订阅
    url(r'^all/rss/$', ArticlesPostRssFeed(), name='rss'),
    path('all/rss/<int:column_id>/', ArticlesPostColumnRssFeed(), name='column_rss'),

    # haystack search
    # url(r'^search/', include('haystack.urls')),

    # allauth
    path('accounts/', include('allauth.urls')),

    path('account/weibo_login_success/', TemplateView.as_view(template_name='account/weibo_login_success.html')),

    # notifications
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    # extends
    path('extends/', include('extends.urls', namespace='extends')),

    # rest-framework login view
    url(r'^api/auth/', include('rest_framework.urls')),

    # api-article
    path('api/article/', include('article.api.urls', namespace='api_article')),

    # api-comments
    path('api/comments/', include('comments.api.urls', namespace='api_comments')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
