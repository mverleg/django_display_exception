
from display_exceptions import BadRequest, PermissionDenied, NotFound
from django.utils.translation import ugettext as _


def raise_bad_request_exception(request):
	exception = BadRequest(
		message = _('Your request could not be understood. If you did not do anything special and you are using up-to-date software, then this could be caused by a small bug in the website. Apologies for the inconvenience.').format(request.get_full_path()),
	)
	return exception.render(request)


def raise_permission_denied_exception(request):
	exception = PermissionDenied(
		message = _('You do not the necessary permission to access this page ({0:s}). Apologies for the inconvenience.').format(request.get_full_path()),
	)
	return exception.render(request)


def raise_not_found_exception(request):
	exception = NotFound(
		message = _('The document you were looking for ({0:s}) was not found. Perhaps there is a mistake in the url, or the document has been moved. Apologies for the inconvenience.').format(request.get_full_path()),
		caption = _('Page not found'),
	)
	return exception.render(request)


