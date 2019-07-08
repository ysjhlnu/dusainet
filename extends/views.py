from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import SiteMessage
from comments.models import Comment
from article.models import ArticlesPost
from album.models import Album
from vlog.models import Vlog

from payjs import PayJS, PayJSNotify
from django.views.decorators.csrf import csrf_exempt

from dusainet2.settings import LOGGING, PAYJS_MCHID, PAYJS_KEY
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

    # 扫码支付
    OUT_TRADE_NO = '20190708TEST'  # 外部订单号（自己的支付系统的订单号，请保证唯一）
    TOTAL_FEE = 1  # 支付金额，单位为分，金额最低 0.01 元最多 10000 元
    BODY = '测试支付'  # 订单标题
    NOTIFY_URL = 'https://www.dusaiphoto.com/extends/payjs/notify/wechat'  # Notify 网址
    ATTACH = 'info'  # Notify 内容
    payjs_response = payjs.QRPay(out_trade_no=OUT_TRADE_NO, total_fee=TOTAL_FEE, body=BODY, notify_url=NOTIFY_URL, attach=ATTACH)
    # if r:
    #     print(r.code_url)  # 二维码地址（weixin:// 开头，请使用此地址构建二维码）
    #     print(r.qrcode)  # 二维码地址（https:// 开头，为二维码图片的地址）
    #     print(r.payjs_order_id)  # 订单号（PAYJS 的）
    # else:
    #     print(r.STATUS_CODE)  # HTTP 请求状态码
    #     print(r.ERROR_NO)  # 错误码
    #     print(r.error_msg)  # 错误信息
    #     print(r)
    context = {
        'payjs_response': payjs_response
    }
    return render(request, 'extends/appreciate.html', context=context)


@csrf_exempt
def payjs_wechat_notify(request):
    if request.method == 'POST':
        payjs = PayJS(PAYJS_MCHID, PAYJS_KEY)
        payjs_check = payjs.check_status(payjs_order_id=request.POST.get('payjs_order_id'))
        print(request.POST, request.POST.get('payjs_order_id'))
        if payjs_check:
            print(payjs_check.paid)
            print('1')
            return JsonResponse({'status': 'T'})
        else:
            print('2')
            print(payjs_check.error_msg)
            return JsonResponse({'status': 'F'})
    else:
        print('3')
        return JsonResponse({'code': 403, 'msg': 'request method must POST.'})