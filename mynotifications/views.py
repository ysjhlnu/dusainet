from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from article.models import ArticlesPost
from readbook.models import ReadBook
from vlog.models import Vlog

from dusainet2.settings import LOGGING
import logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('django.request')

@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification(request):
    """
    通知界面
    """
    unread_notify = request.user.notifications.unread()
    return render(
        request,
        'notifications/my_notification.html',
        {'unread_notify': unread_notify},
    )


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_all_as_read(request):
    """
    标记所有信息为已读
    """
    request.user.notifications.mark_all_as_read()
    return redirect('my_notifications:notify_box')


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_as_read(request,
                                       article_id,
                                       notify_id,
                                       article_type):
    """
    标记点击过的信息为已读
    """
    if article_type == 'article':
        article = get_object_or_404(ArticlesPost, id=article_id)
    elif article_type == 'readbook':
        article = get_object_or_404(ReadBook, id=article_id)
    else:
        article = get_object_or_404(Vlog, id=article_id)
    try:
        request.user.notifications.get(id=notify_id).mark_as_read()
    except:
        logger.warning('comments_notification_mark_as_read: Notification matching query does not exist.\n    request url: {0}'.format(request.path_info))
    return redirect(article)
