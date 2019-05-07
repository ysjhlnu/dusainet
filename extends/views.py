from django.shortcuts import render
from .models import SiteMessage


# def get_latest_site_message(request):
#     message = SiteMessage.objects.last()
#     return render(request, 'extends/site_message_tip.html', {'message': message})
