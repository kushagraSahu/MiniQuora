from django import forms
from django.forms import ModelForm
from .models import Question,Answer

class AddAnswer(ModelForm):
	class Meta:
		model = Answer
		fields = ['text']
			
class AddQues(ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'description']


	def clean_title(self):
		data_title = self.cleaned_data['title']
		if Question.objects.filter(title = data_title):
			forms.ValidationError('This Question Already Exists. Check you Quora feed noob!')
		return data_title

class EditQues(ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'description']


	
