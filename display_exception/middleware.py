
from django.conf import settings
from django.shortcuts import render
from display_exception import DisplayableException


BASE_TEMPLATE = settings.get('DISPLAY_EXCEPTIONS_BASE_TEMPLATE', DisplayableException.default_template)


class DisplayExceptionMiddleware(object):
	def process_exception(self, request, exception):
		if isinstance(exception, DisplayableException):
			response = render(request, exception.template, {
				'exception': exception,
				'header': exception.header,
				'message': exception.message,
			})
			response.status_code = exception.status_code
			return response
		""" return None: exception is handled normally (e.g. shown to user) """
		return None


