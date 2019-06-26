from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import SiteMessage
from comments.models import Comment


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
        return
    obj.likes += 1
    obj.save(update_fields=['likes'])
    return JsonResponse({'state': 200})
