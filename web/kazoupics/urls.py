"""kazoupics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from wall.views import show_pics, next_pic, new_pic, bigscreen, incoming_sms, get_sms, leaderboard, ban, add_ad, del_sms


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^next/$', next_pic, name='next'),
    url(r'^next/(?P<current>.+)/$', next_pic),
    url(r'^newpic/$', new_pic, name='newpic'),
    url(r'^bigscreen/', bigscreen, name='bigscreen'),
    url(r'^incomingsms/$', incoming_sms),
    url(r'^getsms/$', get_sms, name='get_sms'),
    url(r'^leaderboard/$', leaderboard, name='leaderboard'),
    url(r'^ban/(?P<username>.*)/$', ban, name='ban'),
    url(r'^add_ad/$', add_ad, name='add_ad'),
    url(r'^del_sms/(?P<id>[0-9]+)/$', del_sms, name='del_sms'),
    url(r'^$', show_pics, name='show_pics')
]
