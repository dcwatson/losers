from django.conf.urls import include, url
from django.contrib import admin
from .views import pick, login, logout, standings, profile

urlpatterns = [
    url(r'^$', pick, name='pick'),
    url(r'^login/$', login, name='login'),
    url(r'^login/(?P<code>[^/]+)/$', login, name='login-code'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^standings/$', standings, name='standings'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^admin/', include(admin.site.urls)),
]
