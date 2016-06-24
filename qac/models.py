from django.db import models
from account.models import MyUser

# Create your models here.
class Question(models.Model):
	title = models.CharField(max_length=100,default = '')
	description = models.TextField(max_length=500,default = '',blank = True)
	created_by = models.ForeignKey(MyUser, related_name = 'questions_created')
	created_on = models.DateTimeField(auto_now_add = True)
	upvoted_by = models.ManyToManyField(MyUser, related_name = 'questions_upvoted', blank = True)
	def __str__(self):
		return self.title;

class Answer(models.Model):
	text = models.TextField(max_length=100000,default = '')
	question = models.ForeignKey(Question, related_name = 'answers', null = True)
	created_on = models.DateTimeField(auto_now_add = True, null = True)
	answered_by = models.ForeignKey(MyUser, related_name = 'answers_written', null = True)
	def __str__(self):
		return self.text;

class Comment(models.Model):
	comments_text = models.TextField(max_length=200,default = '')
	def __str__(self):
		return self.comments_text;

