from django.urls import path
from . import views

app_name = 'my_notifications'
urlpatterns = [
    path(
        '',
        views.comments_notification,
        name='notify_box',
    ),
    path(
        'mark-all-read',
        views.comments_notification_mark_all_as_read,
        name='mark_all_read',
    ),
    path(
        'mark-as-read/<int:article_id>/<int:notify_id>/<article_type>/',
         views.comments_notification_mark_as_read,
        name='mark_as_read',
    ),
    path(
        'soft-delete-all/',
        views.comments_notification_soft_delete_all,
        name='soft_delete_all',
    ),
]
