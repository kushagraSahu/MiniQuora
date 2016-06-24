from django.db import models
from random import randint
from django.contrib.auth.models import AbstractUser
# Create your models here.
class MyUser(AbstractUser):
    phone = models.CharField(max_length = 10, null = True)
    description = models.CharField(max_length = 40, default = 'Noob')

def create_otp(user = None, purpose = None):
	if not user:
		raise ValueError('Invalid Argument');
	choices = []
	for choice_purpose, verbose in UserOTP.purpose_choices:
		choices.append(choice_purpose)
	if not purpose in choices:
		raise ValueError('Invalid Argument')
	if UserOTP.objects.filter(user = user, purpose = purpose).exists():
		old_otp = UserOTP.objects.get(user = user, purpose = purpose)
		old_otp.delete();
	otp = randint(1000,9999)
	otp_object = UserOTP.objects.create(user = user, purpose = purpose, otp = otp)
	return otp;

def get_valid_otp_object(user = None, purpose = None, otp = None):
	if not user:
		raise ValueError('Invalid Argument')
	choices = []
	for choice_purpose, verbose in UserOTP.purpose_choices:
		choices.append(choice_purpose)
	if not purpose in choices:
		raise ValueError('Invalid Argument')
	try:
		otp_object = UserOTP.objects.get(user = user, purpose = purpose, otp = otp)
		return otp_object
	except UserOTP.DoesNotExist:
		return None;

class UserOTP(models.Model):
	purpose_choices = (
		('FP', 'Forgot Password'),
		('AK', 'Activation Key'),
	);
	user = models.ForeignKey(MyUser)
	otp = models.CharField(max_length = 4)
	purpose = models.CharField(max_length = 2, choices = purpose_choices)
	created_on = models.DateTimeField(auto_now_add = True)
	class Meta:
		unique_together= ['user', 'purpose']




