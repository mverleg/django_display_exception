
"""

"""

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from functions import check_user_access, check_self_only


def user_update_name_allhere(request):
	# first find the user we're trying to edit
	try:
		editing_user = get_user_model().objects.get(**{
			get_user_model().USERNAME_FIELD: request.GET['user']
		})
	except (IndexError, MultiValueDictKeyError):
		return render(request, 'not_found.html', {
			'message': 'A username is needed to look up a user.',
			'next': 'home',
		})
	except get_user_model().DoesNotExist:
		return render(request, 'not_found.html', {
			'message': 'No user by the name "{0:s}".'.format(request.GET['user']),
			'next': 'home',
		})
	# now check that we have permission to edit users
	if not request.user.is_authenticated():
		return render(request, 'permission_denied.html', {
			'message': 'You need to login to be able to do this ("{0:s}").'.format('change_user'),
			'next': 'login',
		})
	if not request.user.has_perm('change_user'):
		return render(request, 'permission_denied.html', {
			'message': 'You do not have permission to this operation ("{0:s}").'.format('change_user'),
			'next': 'home',
		})
	# finally check that we're editing our own account, or that we're a staff member
	if not request.user.pk == editing_user.pk or request.user.is_staff:
		return render(request, 'permission_denied.html', {
			'message': 'You can only edit your own account. You can continue to your own account, or use your browser\'s back button',
			'header': 'Don\'t mess with other people!',
			'next': '{0:s}?user={1:s}'.format(reverse('user_update_email'), request.user.username),
		})
	# handle the name update here
	return HttpResponse('ok')


	def try_to_get_user(dic, key = 'user'):
		try:
			user = get_user_model().objects.get(**{
				get_user_model().USERNAME_FIELD: dic[key]
			})
		except (IndexError, MultiValueDictKeyError):
			return render(request, 'not_found.html', {
				'message': 'A username is needed to look up a user.',
				'next': 'home',
			})
		except get_user_model().DoesNotExist:
			return render(request, 'not_found.html', {
				'message': 'No user by the name "{0:s}".'.format(request.GET['user']),
				'next': 'home',
			})
		return user


def user_update_name_funcs(request):
	# first find the user we're trying to edit
	user_or_error = try_to_get_user(request.GET)
	if not isinstance(user_or_error, get_user_model()):
		return user_or_error
	else:
		user = user_or_error
	# now check that we have permission to edit users & that we're editing our own account, or that we're a staff member
	possible_error_one = check_user_access(request.user, 'change_user')
	possible_error_two = check_self_only(request.user, user)
	if possible_error_one or possible_error_two:
		return possible_error_one or possible_error_two
	# handle the email update here
	return HttpResponse('ok')