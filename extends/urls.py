from django.urls import path
from . import views

app_name = 'extends'
urlpatterns = [
    path('latest-site-message', views.latest_site_message, name='site_message'),
    path('increase-likes/<obj_type>/<int:obj_id>', views.increase_likes, name='increase_likes'),

    path('payjs/qrpay/', views.payjs_QRpay, name='payjs-qrpay'),
    path('payjs/check_payment', views.check_payment, name='check-payment'),
    path('payjs/notify/wechat', views.payjs_wechat_notify, name='payjs-notify-wechat'),
    path('sponsor-list', views.sponsor_list, name='sponsor-list'),
]
