"""EasyTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from EasyTest.settings import DEBUG
from EasyTest.views import index
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', index),
    url('index/', index),
    url(r'^base', include("base.urls")),
    # url(r'^system', include("base.urls")),
]

# 修改 urls.py 因为显示问题，增加 DEBUG 内容
from django.conf.global_settings import STATIC_ROOT

if DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)/$', serve, {"document_root": STATIC_ROOT}),
