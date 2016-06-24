from django.conf.urls import url
from account import views as accountviews
from qac import views as ques_views
from qac.views import all_questions as listques
from qac.views import hello

urlpatterns = [
	#url(r'^hello/$', accountviews.hello),
	url(r'^all/$', listques),
	url(r'^hello/$',hello),
	url(r'^(?P<id>[0-9]+)/$',ques_views.get_question),
	url(r'^add/$', ques_views.add_question, name = 'addquestion'),
	url(r'^save/$',ques_views.save_question),
	url(r'^edit/(?P<id>\d+)$',ques_views.edit_question, name = 'editquestion'),
	url(r'^add-answer/(?P<id>\d+)$',ques_views.add_answer, name = 'addanswer'),

]