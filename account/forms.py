from django import forms
from account.models import MyUser

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 25)
	password = forms.CharField(widget = forms.PasswordInput)
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if not MyUser.objects.filter(username = username).exists():
			raise forms.ValidationError('Invalid Username')
		return username

class ForgotPasswordForm(forms.Form):
	username = forms.CharField(max_length = 25)

	def clean_username(self):
		username = self.cleaned_data.get('username','')
		if username and not MyUser.objects.filter(username = username).exists():
			raise forms.ValidationError('Invalid Username')
		return username;

class ResetPasswordForm(forms.Form):
	new_password = forms.CharField(widget = forms.PasswordInput)
	confirm_password = forms.CharField(widget = forms.PasswordInput)

	def clean_confirm_password(self):
		new_password = self.cleaned_data['new_password']
		if not new_password:
			raise forms.ValidationError('Invalid password')
		confirm_password = self.cleaned_data['confirm_password']
		if (confirm_password!=new_password):
			raise forms.ValidationError('Password fields dont match!')
		return confirm_password;

class SignUpForm(forms.Form):
	firstname = forms.CharField(max_length = 30)
	lastname = forms.CharField(max_length = 30)
	username = forms.CharField(max_length = 30)
	email = forms.EmailField()
	new_password = forms.CharField(widget = forms.PasswordInput)
	confirm_password = forms.CharField(widget = forms.PasswordInput)
	mobile = forms.CharField(max_length = 10)

	def clean_mobile(self):
		mobile = self.cleaned_data.get('mobile','')
		if len(mobile)!=10 or not mobile:
			raise forms.ValidationError('Invalid Mobile Number.')
		return mobile;
	def clean_username(self):
		username = self.cleaned_data.get('username','')
		if MyUser.objects.filter(username = username).exists():
			raise forms.ValidationError('Username already exists')
		return username;
	def clean_confirm_password(self):
		new_password = self.cleaned_data['new_password']
		if not new_password:
			raise forms.ValidationError('Invalid password')
		confirm_password = self.cleaned_data['confirm_password']
		if (confirm_password!=new_password):
			raise forms.ValidationError('Password fields dont match!')
		return confirm_password;

