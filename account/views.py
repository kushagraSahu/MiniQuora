from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ForgotPasswordForm, ResetPasswordForm, SignUpForm
from .models import create_otp, MyUser, get_valid_otp_object
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader
from django.core import serializers
from qac.models import Question

# Create your views here.
@require_http_methods(['GET', 'POST'])
def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('home',kwargs={'id': request.user.id}));
	if request.method == 'GET':
		context = {'form' : LoginForm()};
		return render(request, 'account/auth/login.html',context);
	else:	
		form = LoginForm(request.POST)
		if not form.is_valid():
			return render(request, 'account/auth/login.html',{'form': form});
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = authenticate(username = username, password = password)
		if not user:
			context = {'form' : LoginForm(),'error' : 'Invalid Username/Password'}
			return render(request,'account/auth/login.html',context);
		if not user.is_active:
			context = {'form' : LoginForm(), 'error' : 'Complete your Registration by clicking on the Activation Link sent on your registered email.'};
			return render(request, 'account/auth/login.html',context);
		if user:
			auth_login(request,user)
			return redirect(reverse('home', kwargs={'id': request.user.id}));

def logout(request):
	auth_logout(request)
	return redirect(reverse('login'));

@login_required
def home(request, id):
	context = {'ques_list' : Question.objects.all().order_by('-created_on')}
	return render(request, 'account/auth/loggedin.html',context);

@require_http_methods(['GET', 'POST'])
def forgot_password(request):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs={'id': request.user.id}));
	if request.method == 'POST':
		form = ForgotPasswordForm(request.POST)
		if form.is_valid():
			user = MyUser.objects.get(username = form.cleaned_data['username'])
			otp = create_otp(user = user,purpose = 'FP')
			email_body_context = {'user': user, 'otp': otp}
			body = loader.render_to_string('account/auth/email/forgot_password.txt', email_body_context)
			message = EmailMultiAlternatives("Reset Password", body, settings.EMAIL_HOST_USER,[user.email])
			message.send()
			return render(request, 'account/auth/forgot_email_sent.html', {'user': user});
		else:
			return render(request, 'account/auth/forgot_password.html', {'f' : form});
	else:
		if request.method == 'GET':
			context = { 'f' : ForgotPasswordForm()};
			return render(request, 'account/auth/forgot_password.html', context);

@require_http_methods(['GET', 'POST'])
def signUp(request):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs={'id' : request.user.id}));
	if request.method == 'GET':
		form = SignUpForm()
		context = {'form' : form}
		return render(request, 'account/auth/signup.html',context);
	else:
		form = SignUpForm(request.POST)
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['mobile']
			password = form.cleaned_data['confirm_password']
			user = MyUser.objects.create(username = username, first_name = firstname, last_name = lastname, email = email, phone = phone)
			otp = create_otp(user = user,purpose = 'AK')
			email_body_context = {'user': user, 'otp': otp}
			body = loader.render_to_string('account/auth/email/register_user.txt', email_body_context)
			message = EmailMultiAlternatives("Activation link", body, settings.EMAIL_HOST_USER,[user.email])
			message.send()
			user.set_password(password)
			user.is_active = False
			user.save();
			return render(request,'account/auth/ak_sent.html', {'user' : user})
		else:
			return render(request, 'account/auth/signup.html', {'form' : form});

def activate_user(request, id = None, otp = None):
	user = get_object_or_404(MyUser, id = id);
	user.is_active = True
	user.save();
	data = serializers.serialize('json', [user])
	return HttpResponse(data, content_type = "application/json" );

@require_http_methods(['GET', 'POST'])
def reset_password(request, id = None, otp = None):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs={'id' : request.user.id}));
	user = get_object_or_404(MyUser, id=id);
	otp_object = get_valid_otp_object(user = user, purpose = 'FP', otp = otp)
	if not otp_object:
		raise Http404();
	if request.method == 'GET':
		form = ResetPasswordForm()
	else:
		form = ResetPasswordForm(request.POST)
		if form.is_valid():
			user.set_password(form.cleaned_data['new_password'])
			user.save();
			otp_object.delete();
			return render(request, 'account/auth/set_password_success.html',{'user' : user})		
	context = {'form' : form, 'id' : user.id, 'otp' : otp_object.otp}
	return render(request, 'account/auth/reset_password.html', context);

@require_POST
def google_login(request):
	pass
