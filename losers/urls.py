from django.conf.urls import include, url
from django.contrib import admin
from .views import pick, login, standings

urlpatterns = [
    url(r'^$', pick, name='pick'),
    url(r'^login/$', login, name='login'),
    url(r'^login/(?P<code>[^/]+)/$', login, name='login-code'),
    url(r'^standings/$', standings, name='standings'),
    url(r'^admin/', include(admin.site.urls)),
]
