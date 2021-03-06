"""baccarat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from base import views


urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^play', views.play_page, name='play'),
    url(r'^admin/', admin.site.urls),
    url(r'^options', views.options, name='options'),
    url(r'^simulate', views.simulate, name='simulate'),
    url(r'^login', views.sign_in, name='sign_in'),
    url(r'^logout', views.sign_out, name='sign_out'),
    url(r'^start_sim/(?P<iterations>[0-9]{1,6})/$', views.start_sim, name='start_sim'),
    # url(r'^stop_sim', views.stop_sim, name='stop_sim'),
]


