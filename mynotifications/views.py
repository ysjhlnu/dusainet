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
def comments_notification_soft_delete_all(request):
    """软删除该用户所有通知"""
    request.user.notifications.mark_all_as_deleted(request.user)
    logger.warning('comments_notification_soft_delete_all: soft delete done.\n     request url: {0}'.format(
        request.path_info
    ))
    return redirect('my_notifications:notify_box')


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification(request):
    """通知界面"""
    try:
        unread_notify = request.user.notifications.unread()
        context = {
            'state': '200',
            'unread_notify': unread_notify,
        }
    except:
        context = {
            'state': '500',
            'unread_notify': None
        }
        logger.error(
            'comments_notification: get unread_notify failed.\n    request url: {0}'.format(
                request.path_info
            )
        )
    return render(
        request,
        'notifications/my_notification.html',
        context,
    )


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_all_as_read(request):
    """标记所有信息为已读"""
    request.user.notifications.mark_all_as_read()
    return redirect('my_notifications:notify_box')


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_as_read(request,
                                       article_id,
                                       notify_id,
                                       article_type):
    """标记点击过的信息为已读"""
    if article_type == 'article':
        article = get_object_or_404(ArticlesPost, id=article_id)
    elif article_type == 'readbook':
        article = get_object_or_404(ReadBook, id=article_id)
    else:
        article = get_object_or_404(Vlog, id=article_id)
    try:
        request.user.notifications.get(id=notify_id).mark_as_read()
    except:
        logger.warning(
            'comments_notification_mark_as_read: Notification matching query does not exist.\n    request url: {0}'.format(
                request.path_info))
    return redirect(article)
