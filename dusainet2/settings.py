import os
import pymysql
import django_smtp_ssl
import json

import logging
import django.utils.log
import logging.handlers

pymysql.install_as_MySQLdb()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open('env.json') as env:
    ENV = json.load(env)

SECRET_KEY = ENV['SECRET_KEY']

if ENV.get('ENV') == 'dev':
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost ', '.dusaiphoto.com', '.dusai.net', ENV.get('ALIYUN_IP')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/dusainet.log'),
            'formatter': 'verbose',
            'when': 'midnight',
            'backupCount': 30,
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        # }
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['file'],
        #     'level': 'WARNING',
        #     'propagate': True,
        # },
        'django.request': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

INSTALLED_APPS = [
    # admin增强
    'jet.dashboard',
    'jet',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'userinfo',
    'article',  # 文章
    'comments',  # 评论
    'album',  # 相册
    'course',  # 教程
    'readbook',  # 读书
    'imagesource',  # 图库
    'vlog',  # 视频
    'aboutme',  # 作者
    'extends',

    'utils',  # 工具

    # django-allauth
    # 必须安装的app
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 下面是第三方账号相关的，选了weibo和github
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.github',

    # 标签
    'taggit',

    # mptt
    'mptt',

    # notifications
    'notifications',
    'mynotifications',

    # haystack search
    # 'haystack',

    # 富文本编辑器
    'ckeditor',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # cor-headers
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dusainet2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dusainet2.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    MYSQL_PASSWORD = ENV.get('MYSQL_KEY')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dusainet2',
            'USER': 'root',
            'PASSWORD': MYSQL_PASSWORD,
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'nginx_static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# django-allauth相关设置
AUTHENTICATION_BACKENDS = (
    # django admin所使用的用户登录与django-allauth无关
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

# Email setting
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = 'dusaiphoto@foxmail.com'
EMAIL_HOST_PASSWORD = ENV.get('EMAIL_HOST_KEY')
EMAIL_PORT = 465

SERVER_EMAIL = 'dusaiphoto@foxmail.com'
DEFAULT_FROM_EMAIL = 'dusaiphoto@foxmail.com'
ADMINS = (('杜赛', 'dusaiphoto@foxmail.com'),)

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '杜赛的个人网站 <dusaiphoto@foxmail.com>'
LOGIN_REDIRECT_URL = '/'
SITE_ID = 1

# haystack相关配置
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'article.whoosh_cn_backend.WhooshEngine',
#         'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
#     },
# }
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

# CORS_ORIGIN_ALLOW_ALL = True
# ckeditor
CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用配置
    'default': {
        'language': 'zh-hans',
        'width': 'auto',
        'height': '250px',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Smiley', 'CodeSnippet', '-', 'Bold',
             'Italic', 'Underline', 'RemoveFormat', ],
            ['NumberedList', 'BulletedList'],
            ['TextColor', 'BGColor'],
            ['Link', 'Unlink'],
            ['Undo', 'Redo', 'Marker'],
            ['Maximize']
        ],
        # 插件
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils', ]),
    }
}

DJANGO_NOTIFICATIONS_CONFIG = {'SOFT_DELETE': True}
