
from django.conf.urls import include, url
from django.contrib import admin
from display_exception import PermissionDenied, NotFound, BadRequest, Notification, NotYetImplemented
from test_app.views_with import home, login, user_update_name, user_update_email, user_show, preview_exception


urlpatterns = [
	url(r'^$', home, name = 'home'),
	url(r'^login/$', login, name = 'login'),
	url(r'^user/name/$', user_update_name, name = 'user_update_name'),
	url(r'^user/email/$', user_update_email, name = 'user_update_email'),
	url(r'^user/show/$', user_show, name = 'user_show'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^permission_denied/$', preview_exception, {'Ex': PermissionDenied}, name = 'permission_denied'),
	url(r'^not_found/$', preview_exception, {'Ex': NotFound}, name = 'not_found'),
	url(r'^not_implemented/$', preview_exception, {'Ex': NotYetImplemented}, name = 'not_implemented'),
	url(r'^bad_request/$', preview_exception, {'Ex': BadRequest}, name = 'bad_request'),
	url(r'^notification/$', preview_exception, {'Ex': Notification}, name = 'notification'),
]


