from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from article.models import ArticlesPost


class SiteMessage(models.Model):
    """通知小贴条"""
    content = models.TextField(verbose_name="正文")
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = '通知'

    def __str__(self):
        return self.content[:20]


class Payment(models.Model):
    """支付"""
    # 支付用户
    user = models.ForeignKey(
        User,
        related_name='payment',
        on_delete=models.SET_NULL,
        verbose_name='用户',
        blank=True,
        null=True
    )

    username = models.CharField(max_length=20, blank=True)

    # 支付来源文章
    paid_for_article = models.ForeignKey(
        ArticlesPost,
        related_name='payment',
        on_delete=models.SET_NULL,
        verbose_name='被赞赏文章',
        blank=True,
        null=True
    )

    # T: 支付成功  F: 支付未成功
    is_paid = models.CharField(max_length=10, default='F')
    # 金额。单位：分
    total_fee = models.IntegerField(default=0)
    # 用户端自主生成的订单号
    out_trade_no = models.CharField(max_length=100)
    # PAYJS 平台订单号
    payjs_order_id = models.CharField(max_length=100)
    # 留空表示微信支付。支付宝交易传值：alipay
    type = models.CharField(max_length=100, default='wechat')
    # 订单标题
    body = models.CharField(max_length=100, blank=True)
    # 用户自定义数据
    attach = models.CharField(max_length=200, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 支付留言
    message = models.CharField(max_length=70, blank=True)

    class Meta:
        verbose_name_plural = '支付'
        ordering = ('-created',)

    def __str__(self):
        return self.payjs_order_id
