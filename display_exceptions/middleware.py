
from display_exceptions import DisplayableException


class DisplayExceptionMiddleware(object):
	def __init__(self, get_response):
		# when using MIDDLEWARE
		self.get_response = get_response
	
	def __call__(self, request):
		# when using MIDDLEWARE
		try:
			resp = self.get_response(request)
		except DisplayableException as exception:
			resp = exception.render(request)
		return resp
	
	def process_exception(self, request, exception):
		# when using MIDDLEWARE_CLASSES
		if isinstance(exception, DisplayableException):
			return exception.render(request)
		""" return None: exception is handled normally (e.g. shown to user) """
		return None


