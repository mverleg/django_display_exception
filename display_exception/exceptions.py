
"""
	Http error descriptions from
	http://www.smartlabsoftware.com/ref/http-status-codes.htm
"""

from django.utils.translation import ugettext_lazy as _


class DisplayableException(Exception):
	"""
		Exceptions derived from this class will be caught and shown to the user.
	"""
	default_status_code = 200
	default_template = 'exceptions/base.html'
	default_header = _('Please note...')

	def __init__(self, message, header = None, next = None, status_code = None, template = None, context = None, *err_args, **err_kwargs):
		"""
			Create a displayable exception.

			:param message: The message to be displayed, describing what went wrong.
			:param header: If set, overrules the default header for the error display page.
			:param next: The url of the page the user should continue, or a callable to generate said url.
			:param status_code: If set, overrules the default http status code of this exception.
			:param template: If set, overrules the default template used to render this exception.
			:param context: Any extra context for the template (only useful for custom templates).
			:param err_args: Positional aguments to be passed on to Exception.
			:param err_kwargs: Keyword arguments to be passed on to Exception.
			:return:

			Argument order may change; use keyword arguments for any arguments other than message and header.
		"""
		super(DisplayableException, self).__init__(*err_args, **err_kwargs)
		self.message = message
		if callable(next):
			self.next = next() if callable(next) else next
		self.header = header or self.default_header
		self.status_code = status_code or self.default_status_code
		self.template = template or self.default_template
		self.context = context or {}


class Notification(Exception):
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
	default_header = _('Permission denied')


class NotFound(DisplayableException):
	"""
		404 Not Found

		The server has not found anything matching the Request-URI.
		No indication is given of whether the condition is temporary or permanent.
	"""
	default_status_code = 404
	default_template = 'exceptions/not_found.html'
	default_header = _('Not found')


class NotImplemented(DisplayableException):
	"""
		501 Not Implemented

		The server does not support the functionality required to fulfill the request.
	"""
	default_status_code = 501
	default_template = 'exceptions/not_implemented.html'
	default_header = _('Not implemented (yet)')


