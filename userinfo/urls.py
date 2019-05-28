from django.urls import path

from . import views

app_name = 'userinfo'
urlpatterns = [
    path('detail/', views.UserInfoView.as_view(), name='detail'),
    path('crop-upload-image/', views.crop_upload_handler, name='crop_upload_image'),
    path('user-signup-validate', views.user_signup_validate, name='user_signup_validate'),
]
