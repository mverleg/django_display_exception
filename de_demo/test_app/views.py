
from django.http import HttpResponse
from django.shortcuts import render
from display_exception import PermissionDenied, NotImplemented
from functions import try_to_get_user, check_user_access, check_self_only


def home(request):
	return render(request, 'home.html')


def login(request):
	raise NotImplemented('Logging in is a top prioriy for us and we\'ll try to get it working a.s.a.p.!', next = 'home', template = None, context = None)


def user_update_name(request):
	user = try_to_get_user(request.GET)
	check_user_access(request.user, 'change_user')
	check_self_only(request.user, user)
	# handle the name update here
	return HttpResponse('ok')


def user_update_email(request):
	user = try_to_get_user(request.GET)
	check_user_access(request.user, 'change_user')
	check_self_only(request.user, user)
	# handle the email update here
	return HttpResponse('ok')


def user_show(request):
	user = try_to_get_user(request.GET)
	return render(request, 'show_user.html', {'user': user})
	# note that things like database errors and non-existent templates
	# still cause a crash and logging etc like normally; they are not
	# displayed to the user (except in DEBUG mode as always).

