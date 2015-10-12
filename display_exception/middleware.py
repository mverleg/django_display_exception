
from django.conf import settings
from django.shortcuts import render
from display_exception import DisplayableException


BASE_TEMPLATE = getattr(settings, 'DISPLAY_EXCEPTIONS_BASE_TEMPLATE', DisplayableException.default_template)


class DisplayExceptionMiddleware(object):
	def process_exception(self, request, exception):
		if isinstance(exception, DisplayableException):
			context = {
				'exception': exception,
				'header': exception.header,
				'message': exception.message,
				'next': next,
				'BASE_TEMPLATE': BASE_TEMPLATE,
			}
			context.update(exception.context)
			response = render(request, exception.template, context)
			response.status_code = exception.status_code
			return response
		""" return None: exception is handled normally (e.g. shown to user) """
		return None


