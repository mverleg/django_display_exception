
from display_exception import DisplayableException


class DisplayExceptionMiddleware(object):
	def process_exception(self, request, exception):
		if isinstance(exception, DisplayableException):
			return exception.render(request, exception)
		""" return None: exception is handled normally (e.g. shown to user) """
		return None


