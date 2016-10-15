
"""
	Http error descriptions from
	http://www.smartlabsoftware.com/ref/http-status-codes.htm
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from importlib import import_module


BASE_TEMPLATE = getattr(settings, 'DISPLAY_EXCEPTIONS_BASE_TEMPLATE', 'exceptions/base.html')


render_func = None
render_func_name = getattr(settings, 'DISPLAY_EXCEPTIONS_RENDER_FUNC', '').rsplit('.', 1)
if len(render_func_name) > 1:
	try:
		render_func = getattr(import_module(render_func_name[0]), render_func_name[1])
	except (ImportError, AttributeError):
		raise ImproperlyConfigured('DISPLAY_EXCEPTIONS_RENDER_FUNC is set to {0:} which cannot be imported'.format(render_func_name))


class DisplayableException(Exception):
	"""
		Exceptions derived from this class will be caught and shown to the user.
	"""
	default_status_code = 200
	default_template = BASE_TEMPLATE

	def __init__(self, message, caption = None, next = None, status_code = None, template = None, context = None, *err_args, **err_kwargs):
		"""
			Create a displayable exception.

			:param message: The message to be displayed, describing what went wrong.
			:param caption: If set, overrules the default header for the error display page.
			:param next: The url of the page the user should continue, or a callable to generate said url.
			:param status_code: If set, overrules the default http status code of this exception.
			:param template: If set, overrules the default template used to render this exception.
			:param context: Any extra context for the template (only useful for custom templates).
			:param err_args: Positional arguments to be passed on to Exception.
			:param err_kwargs: Keyword arguments to be passed on to Exception.
			:return:

			Argument order may change; use keyword arguments for any arguments other than message and caption.
		"""
		super(DisplayableException, self).__init__(*err_args, **err_kwargs)
		self.message = message
		self.caption = caption
		self.next = next() if callable(next) else next
		self.status_code = status_code or self.default_status_code
		self.template = template or self.default_template
		self.context = context or {}

	def render(self, request):
		if render_func:
			return render_func(request, self, template=BASE_TEMPLATE)
		context = {
			'exception': self,
			'caption': self.caption,
			'message': self.message,
			'next': self.next,
			'EXCEPTION_BASE_TEMPLATE': BASE_TEMPLATE,
			'LOGIN_URL': settings.LOGIN_URL,
		}
		context.update(self.context)
		response = render(request, self.template, context)
		response.status_code = self.status_code
		return response


class Notification(DisplayableException):
	"""
		200 Ok

		The request has succeeded. The information returned with the response
		is dependent on the method used in the request.

		It is somewhat doubtful whether you should use an exception for this,
		but it'll work so it's up to you, we're all adults here (maybe).
	"""
	default_template = 'exceptions/notification.html'


class PermissionDenied(DisplayableException):
	"""
		550 Permission Denied

		The server is stating the account you have currently logged in as does not
		have permission to perform the action you are attempting.
	"""
	default_status_code = 550
	default_template = 'exceptions/permission_denied.html'


class BadRequest(DisplayableException):
	"""
		400 Bad Request

		The request could not be understood by the server due to malformed syntax.
		The client should not repeat the request without modifications.
	"""
	default_status_code = 400
	default_template = 'exceptions/bad_request.html'


class NotFound(DisplayableException):
	"""
		404 Not Found

		The server has not found anything matching the Request-URI.
		No indication is given of whether the condition is temporary or permanent.
	"""
	default_status_code = 404
	default_template = 'exceptions/not_found.html'


class NotYetImplemented(DisplayableException):
	"""
		501 Not Implemented

		The server does not support the functionality required to fulfill the request.
	"""
	default_status_code = 501
	default_template = 'exceptions/not_implemented.html'


