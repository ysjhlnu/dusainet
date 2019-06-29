from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import SiteMessage
from comments.models import Comment

from dusainet2.settings import LOGGING
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
    print(type(obj_type), type(obj_id))
    if obj_type == 'comment':
        obj = get_object_or_404(Comment, id=obj_id)
    else:
        logger.error(
            'extends increase_likes: get object went wrong.\n    request url: {0}'.format(
                request.path_info
            )
        )
        return JsonResponse({'state': 500})
    obj.likes += 1
    obj.save(update_fields=['likes'])
    return JsonResponse({'state': 200})
