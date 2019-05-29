from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password

from .forms import PhotoForm
from .models import UserInfo, get_default_avatar_url
from .forms import UserInfoForm

from allauth.account.views import EmailView
from braces.views import LoginRequiredMixin

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress


def user_signup_validate(request):
    """登录/注册验证"""
    data = request.POST
    on_validate_type = data.get('type')

    # signup
    if on_validate_type == 'username':
        if User.objects.filter(username__iexact=data.get('username')).exists():
            return HttpResponse('403')
    elif on_validate_type == 'email':
        if EmailAddress.objects.filter(email__iexact=data.get('email')).exists():
            return HttpResponse('403')

    # login
    elif on_validate_type == 'login':
        password = data.get('password')

        if User.objects.filter(username__iexact=data.get('login')).exists():
            user = User.objects.get(username__iexact=data.get('login'))
            if check_password(password, user.password):
                return HttpResponse('200')
            else:
                return HttpResponse('403')

        elif EmailAddress.objects.filter(email__iexact=data.get('login')).exists():
            user = EmailAddress.objects.get(email__iexact=data.get('login')).user
            if check_password(password, user.password):
                return HttpResponse('200')
            else:
                return HttpResponse('403')

        else:
            return HttpResponse('403')

    return HttpResponse('200')


class UserInfoView(LoginRequiredMixin, EmailView):
    """
    展示个人信息
    """
    success_url = reverse_lazy('userinfo:detail')
    login_url = "/accounts/login"

    def get_context_data(self, **kwargs):
        """
        添加或新建userinfo上下文
        """
        context = super(UserInfoView, self).get_context_data(**kwargs)
        user_id = self.request.user.id

        try:
            userinfo = UserInfo.objects.get(user_id=user_id)

        except:
            userinfo = UserInfo.objects.create(user_id=user_id)

        if not userinfo.avatar:
            userinfo.avatar = get_default_avatar_url()
            userinfo.save()

        userinfo_form = UserInfoForm()
        data = {
            'userinfo': userinfo,
            'userinfo_form': userinfo_form,
        }
        context.update(data)

        return context


@login_required(login_url='/accounts/login')
def crop_upload_handler(request):
    """
    裁剪并上传用户头像
    """
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user.id
            form.save(user_id=user_id)
    return redirect('userinfo:detail')
