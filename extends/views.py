from django.http import JsonResponse
from .models import SiteMessage


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
