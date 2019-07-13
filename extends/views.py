from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import SiteMessage, Payment
from comments.models import Comment
from article.models import ArticlesPost
from album.models import Album
from vlog.models import Vlog

from payjs import PayJS, PayJSNotify
from django.views.decorators.csrf import csrf_exempt
from utils.templatetags.filter_utils import time_since_zh


from dusainet2.settings import LOGGING, PAYJS_MCHID, PAYJS_KEY, PAYJS_NOTIFY_URL
from time import strftime, localtime
from random import randint

import logging

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('django.request')


# 获取最后一条站通知
def latest_site_message(request):
    try:
        message = SiteMessage.objects.last()
        data = {
            'content': message.content.replace("\r\n", "<br/>"),
            'created': message.created.strftime("%Y/%m/%d"),
        }
    except:
        data = {
            "content": "o(╥﹏╥)o服务器连接失败~"
        }
    return JsonResponse(data, safe=True)


# 点赞计数
def increase_likes(request, obj_type, obj_id):
    response = {}
    if obj_type == 'comment':
        obj = get_object_or_404(Comment, id=obj_id)
        response.update({'node_type': 'comment'})
    elif obj_type == 'article':
        obj = get_object_or_404(ArticlesPost, id=obj_id)
        response.update({'node_type': 'article'})
    elif obj_type == 'album':
        obj = get_object_or_404(Album, id=obj_id)
        response.update({'node_type': 'album'})
    elif obj_type == 'vlog':
        obj = get_object_or_404(Vlog, id=obj_id)
        response.update({'node_type': 'vlog'})
    else:
        logger.error(
            'extends increase_likes: get object went wrong.\n    request url: {0}'.format(
                request.path_info
            )
        )
        return JsonResponse({'state': 500})

    obj.likes += 1
    obj.save(update_fields=['likes'])
    response.update({'state': 200})
    return JsonResponse(response)


def payjs_QRpay(request):
    # 初始化
    payjs = PayJS(PAYJS_MCHID, PAYJS_KEY)
    try:
        total_fee = int(request.POST.get('total_fee'))
        username = request.POST.get('username')
        message = request.POST.get('message')
    except:
        logger.error('extends payjs_QRpay: get total_fee failed.')
        total_fee = 3000
        username = '[匿名用户]'
        message = '小小赞赏鼓励博主'

    # 扫码支付
    OUT_TRADE_NO = strftime("%Y%m%d%H%M%S", localtime()) + '-{}'.format(randint(10000, 99999))
    TOTAL_FEE = total_fee
    BODY = '文章赞赏'
    NOTIFY_URL = PAYJS_NOTIFY_URL

    payjs_response = payjs.QRPay(
        out_trade_no=OUT_TRADE_NO,
        total_fee=TOTAL_FEE,
        body=BODY,
        notify_url=NOTIFY_URL,
    )

    if payjs_response:
        payment = Payment.objects.create(
            total_fee=TOTAL_FEE,
            out_trade_no=OUT_TRADE_NO,
            payjs_order_id=payjs_response.payjs_order_id,
            body=BODY,
        )
        payment.username = username
        payment.message = message
        payment.save()
    else:
        logger.error(
            'extends payjs_QRpay: get QRPay error.\n    code: {0}  error_no: {1}  error_msg: {2}'.format(
                payjs_response.STATUS_CODE,
                payjs_response.ERROR_NO,
                payjs_response.error_msg
            )
        )
    context = {
        'payjs_response': payjs_response
    }
    return render(request, 'extends/appreciate.html', context=context)


@csrf_exempt
def check_payment(request):
    if request.method == 'POST':
        payjs_order_id = request.POST.get('payjs_order_id')
        try:
            payment = Payment.objects.get(payjs_order_id=payjs_order_id)
        except:
            logger.error('extends check_payment_is_paid: get payment failed.')
            return JsonResponse({'status': 500})

        if payment.is_paid == 'T':
            return JsonResponse({'status': 200, 'is_paid': 'T'})
        else:
            return JsonResponse({'status': 200, 'is_paid': 'F'})


@csrf_exempt
def payjs_wechat_notify(request):
    if request.method == 'POST':
        payjs_order_id = request.POST.get('payjs_order_id')
        return_code = request.POST.get('return_code')
        if return_code == 1:
            try:
                payment = Payment.objects.get(payjs_order_id=payjs_order_id)
                payment.is_paid = 'T'
                payment.save()
            except:
                logger.error('extends payjs_wechat_notify: get payment failed.')



def sponsor_list(request):
    sponsors = Payment.objects.filter(is_paid='T').order_by('-created')
    if request.is_ajax() and request.method == 'GET':
        data = []
        for sponsor in sponsors[:10]:
            data.append({
                'total_fee': int(sponsor.total_fee / 100),
                'username': sponsor.username,
                'message': sponsor.message,
                'created': time_since_zh(sponsor.created)
            })
        return JsonResponse({'sponsors': data})
    return render(request, 'extends/sponsor_list.html', {'sponsors': sponsors})
