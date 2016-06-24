from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Answer
from .forms import EditQues, AddQues, AddAnswer
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse




# Create your views here.

def hello(request):
	return HttpResponse('<h1>Hello</h1>')
@csrf_exempt
def all_questions(request):
	context = {'q_list' : Question.objects.all()}
	return render(request,'qac/index.html',context)

@require_GET
@csrf_exempt
def get_question(request, id = None):
	if not id:
		raise Http404
	q = get_object_or_404(Question, id = id)
	'''
	if we want to include fields of our choices in the object, we write the following code:
	data = { 'id' = q.id, 'title = q.title', 'description' = q.description}
	return JsonResponse(data); #JsonResponse py dictionary ko Json me convert kar deta hai
	'''
	#Agar poora object bhejna hain as a JsonResponse, we first serialize it into a Json String and then return it as a HttpResponse!
	data = serializers.serialize('json', [q]);#second argument is always list of objects.
	#if I now return a JsonResponse, there will double serialisation of data, so to avoid this, just return a HttpResponse where the content type will be json.
	return HttpResponse(data, content_type = "application/json" );

@require_POST
def save_question(request):
    title = request.POST.get('title' , '')
    if not title:
        raise Http404
    description = request.POST.get('description' , '')
    q = Question.objects.create(title = title, description = description, created_by = request.user);
    return HttpResponse('ok');

@require_http_methods(['GET','POST'])
def add_question(request):
	if request.method == 'GET':	
		form = AddQues()
		context = {'form' : form}
		return render(request, 'qac/add_question.html',context)
	else:
		form = AddQues(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			question_obj = Question.objects.create(title = title, description = description, created_by = request.user)
			question_obj.save();
			return redirect(reverse('home', kwargs={'id': request.user.id}));
		else:
			return render(request, 'qac/add_question.html',{'form':form})

@require_http_methods(['GET', 'POST'])
def edit_question(request, id = None):
	if request.method == 'GET':	
		form = EditQues()
		question_obj = Question.objects.get(id = id)
		context = {'form' : form, 'question': question_obj}
		return render(request, 'qac/edit_question.html',context)
	else:
		form = EditQues(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			question_obj = Question.objects.get(id = id)
			question_obj.title = title;
			question_obj.description = description;
			question_obj.save();
			return redirect(reverse('home', kwargs={'id': request.user.id}));
		else:
			return render(request, 'qac/edit_question.html',{'form':form})

@require_http_methods(['GET','POST'])
def add_answer(request, id = None):
	if request.method == 'GET':	
		form = AddAnswer()
		question = Question.objects.get(id = id)
		context = {'form' : form, 'question' : question}
		return render(request, 'qac/add_answer.html',context)
	else:
		form = AddAnswer(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text']
			question_obj = Question.objects.get(id=id)
			answer_obj = Answer.objects.create(text = text, question = question_obj, answered_by = request.user)
			answer_obj.save();
			return redirect(reverse('home', kwargs={'id': request.user.id}));
		else:
			return render(request, 'qac/add_question.html',{'form':form})

