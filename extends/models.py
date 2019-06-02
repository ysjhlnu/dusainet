from django.db import models
from django.utils import timezone


class SiteMessage(models.Model):
    """通知小贴条"""
    content = models.TextField(verbose_name="正文")
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = '通知'

    def __str__(self):
        return self.content[:20]

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            print('success')
        except BaseException as e:
            print('SiteMessage_error')
            print(e)
