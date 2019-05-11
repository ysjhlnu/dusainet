from django.http import JsonResponse
from .models import SiteMessage


def latest_site_message(request):
    message = SiteMessage.objects.last()
    data = {
        'content': message.content.replace("\r\n", "<br/>"),
        'created': message.created.strftime("%Y/%m/%d"),
    }
    return JsonResponse(data, safe=True)
