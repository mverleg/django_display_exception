
from django.conf.urls import include, url
from django.contrib import admin
from test_app.views_with import home, login, user_update_name, user_update_email, user_show


urlpatterns = [
    url(r'^$', home, name = 'home'),
    url(r'^login/$', login, name = 'login'),
    url(r'^user/name/$', user_update_name, name = 'user_update_name'),
    url(r'^user/email/$', user_update_email, name = 'user_update_email'),
    url(r'^user/show/$', user_show, name = 'user_show'),
    url(r'^admin/', include(admin.site.urls)),
]


