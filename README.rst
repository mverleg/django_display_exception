Django Display Exceptions
---------------------------------------

This app can (slightly) encourage modularity and readability, as well as decrease code repetition and length, by using Exceptions to handle exceptional (non-standard) situations.

Specifically, it offers an alternative way to handle a failing check in a view fails (object not found, access denied, etc). It let's you throw an special exception that is shown to the user in a pretty way. No need to worry about returning error messages up the chain.

The 'problem' (or 'inconvenience' really) that this solves is explained in my programmers.stackexchange_ question, which is where the idea for started.

Example usage
---------------------------------------

There is a simple example (the whole app is simple, really) contained in the de_demo directory of this repository. For a preview, check the last code block in this subsection.

Let's say you have an app and you want to be able to edit some object belonging to a user, like their account. Normally you would do something like::

	def user_update_name(request):
		# first find the user we're trying to edit
		try:
			editing_user = get_user_model().objects.get(**{
				get_user_model().USERNAME_FIELD: request.GET['user']
			})
		except (IndexError, MultiValueDictKeyError):
			return render(request, 'not_found.html', {
				'message': 'A username is needed to look up a user.',
				'next': reverse('home'),
			})
		except get_user_model().DoesNotExist:
			return render(request, 'not_found.html', {
				'message': 'No user by the name "{0:s}".'.format(request.GET['user']),
				'next': reverse('home'),
			})
		# now check that we have permission to edit users
		if not request.user.is_authenticated():
			return render(request, 'permission_denied.html', {
				'message': 'You need to login to be able to do this ("{0:s}").'.format('change_user'),
				'next': reverse('login'),
			})
		if not request.user.has_perm('change_user'):
			return render(request, 'permission_denied.html', {
				'message': 'You do not have permission to this operation ("{0:s}").'.format('change_user'),
				'next': reverse('home'),
			})
		# finally check that we're editing our own account, or that we're a staff member
		if not request.user.pk == editing_user.pk or request.user.is_staff:
			return render(request, 'permission_denied.html', {
				'message': 'You can only edit your own account. You can continue to your own account, or use your browser\'s back button',
				'header': 'Don\'t mess with other people!',
				'next': '{0:s}?user={1:s}'.format(reverse('user_update_email'), request.user.username),
			})
		# handle the name update here

Looks secure! But now we want another view to update the name. Also we'll want to view users, which only requires the first set of checks. So we make some functions, to not repeat ourselves::

	# one of the functions (others are implied)
	def try_to_get_user(dic, key = 'user'):
		try:
			user = get_user_model().objects.get(**{
				get_user_model().USERNAME_FIELD: dic[key]
			})
		except (IndexError, MultiValueDictKeyError):
			return render(request, 'not_found.html', {
				'message': 'A username is needed to look up a user.',
				'next': reverse('home'),
			})
		except get_user_model().DoesNotExist:
			return render(request, 'not_found.html', {
				'message': 'No user by the name "{0:s}".'.format(request.GET['user']),
				'next': reverse('home'),
			})
		return user

	# the updated view; note that user_update_email looks almost identical
	def user_update_name(request):
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

That is a bit better, but there's still a lot of checking going on in our views. And the dynamic typing abuse isn't exactly beautiful.

So maybe we can handle the exceptional situations using Exceptions? If we use normal ones, we have to catch them in the main view, which will have us repeat a lot of code again. So this is where Django Display Exceptions comes in! We simply raise displayable exceptions::

	# one of the functions (others are implied)
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

	# the twice updated view; note that user_update_email looks almost identical
	def user_update_email(request):
		user = try_to_get_user(request.GET)
		check_user_access(request.user, 'change_user')
		check_self_only(request.user, user)
		# handle the email update here

*Shorter, more readable, almost no code repetition and no dynamic typing abuse*!

Note that these are special exceptions. If some other error occurs, it will be handled just like it normally would; it will not be rendered by Django Display Exceptions.

Configuration
---------------------------------------

I know what you're thinking: *by the gods, this is genius, I want in on this!*

Setup is easy: install with pip in your virtual environment (or globally, I won't judge)::

	pip install django_display_exceptions

Second, add ``display_exceptions`` to ``INSTALLED_APPS``::

	INSTALLED_APPS = (
		'display_exceptions',
		...
	)

If you want to override the exception templates, you will have to place the override app below ``display_exceptions``. That's the only condition, so might as well place ``display_exceptions`` somewhere at the top.

Third, add the middleware that will handle displaying the exceptions::

	MIDDLEWARE_CLASSES = (
		...
		'display_exceptions.DisplayExceptionMiddleware',
	)

In this case, you probably want Django Display Exceptions to do it's thing before before any logging or fallbacks or anything. This means that it should be below any such middleware (since it's an exception, which are handled in the same order as responses). So put it somewhere at the bottom.

There are no migrations. In production, if you want to use the default templates, you'll have to call ``collectstatic``.

That is all; you're good to go!

Built-in displayable exceptions
---------------------------------------

The exceptions that are built in, and that are caught by the middleware:

* *PermissionDenied* (550 Permission Denied): the current account doesn't have access to this resource.
* *NotFound* (404 Not Found): whatever the user requested could not be found (temporarily or permanently).
* *BadRequest* (400 BadRequest): what the user sent is not correctly formatted (e.g. non-integer id).
* *NotYetImplemented* (501 Not Implemented): the requested functionality isn't supported yet.
* *Notification* (200 Ok): no error, just display something.

If there's no suitable exception in the list, you can subclass ``DisplayableException`` yourself.

Arguments
---------------------------------------

The exceptions take several arguments that influence their rendering:

* *message*: The message to be displayed, describing what went wrong.
* *caption*: If set, overrules the default caption for the error display page.
* *next*: The url of the page the user should continue, or a callable to generate said url.
* *status_code*: If set, overrules the default http status code of this exception.
* *template*: If set, overrules the default template used to render this exception.
* *context*: Any extra context for the template (only useful for custom templates).

Check out the docstring for ``DisplayableException`` for all the arguments.

Customization
---------------------------------------

The above arguments are useful for per-exception customization, but perhaps you want to integrate the overall look into your site. There are several options.

You can change the base template used for exceptions in settings::

	DISPLAY_EXCEPTIONS_BASE_TEMPLATE = 'exceptions/base.html'

Unless you're also overriding all the derived templates, your base template should contain the blocks ``caption``, ``message``, `icon`` and ```actions`` (for buttons).

You can also override templates for each of the exceptions. Just create a file called for example ``exceptions/permission_denied.html`` (see notes for ``INSTALLED_APPS`` order). If you want to use the exception base template, these templates should::

	{% extends EXCEPTION_BASE_TEMPLATE %}

and implement the blocks mentioned.

Finally, you can change the rendering function, using ``settings.DISPLAY_EXCEPTIONS_RENDER_FUNC``. It should accept ``request``, ``exception`` and any ``**kwargs`` (forward compatibility).

Handling standard problems
---------------------------------------

This app is not intended for handling real, unexpected problems, which is why internal server errors aren't included.

That said, if you want some placeholder error handlers anyway, you can put this in your root `urls.py`::

	handler400 = raise_bad_request_exception
	handler403 = raise_permission_denied_exception
	handler404 = raise_not_found_exception

Remember that these only appear if `DEBUG = False`.

License
---------------------------------------

Revised BSD License; at your own risk, you can mostly do whatever you want with this code, just don't use my name for promotion and do keep the license file.

.. _programmers.stackexchange: http://programmers.stackexchange.com/questions/276302/how-to-handle-django-get-single-instance-in-view-pattern


