
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from display_exceptions import PermissionDenied, NotFound


def try_to_get_user(dic, key = 'user'):
	try:
		user = get_user_model().objects.get(**{
			get_user_model().USERNAME_FIELD: dic[key]
		})
	except (IndexError, MultiValueDictKeyError):
		raise NotFound('A username is needed to look up a user.', next = reverse('home'))
	except get_user_model().DoesNotExist:
		raise NotFound('No user by the name "{0:s}".'.format(dic[key]), next = reverse('home'))
	return user


def check_user_access(user, perm_code = 'change_user'):
	if not user.is_authenticated():q
		raise PermissionDenied('You need to login to be able to do this ("{0:s}").'.format(perm_code), next = reverse('login'))
	if not user.has_perm(perm_code):
		raise PermissionDenied('You do not have permission to this operation ("{0:s}").'.format(perm_code), next = reverse('home'))


def check_self_only(active_user, subject_user):
	if not active_user.pk == subject_user.pk or active_user.is_staff:
		raise PermissionDenied(
			'You can only edit your own account. You can continue to your own account, or use your browser\'s back button',
			header = 'Don\'t mess with other people!',
			# notice that we use a lambda function for next because we only want to reverse if the exception actually occurs
			# we could just pass the url (which is easier) at a small performance hit, this is also accepted
			next = lambda: '{0:s}?user={1:s}'.format(reverse('user_update_email'), active_user.username)
		)


