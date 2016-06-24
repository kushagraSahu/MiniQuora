from django.contrib import admin
from .models import Question
from .models import Answer
from .models import Comment

#admin.site.register(Question)
#admin.site.register(Answer)
#admin.site.register(Comment)
#Customization['']
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ['title','description']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ['text','question','answered_by']

# Register your models here.
