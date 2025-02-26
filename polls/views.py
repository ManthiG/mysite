from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from django.template import loader 
from django.urls import reverse
from django.db.models import F

from .models import Choice, Question
from django.shortcuts import get_object_or_404, render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,"polls/detail.html", {"question":question})    

def vote (request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except(KeyError,Choice.DoesNotExist):
        return render (request,"polls/detail.html",{"question":question,"error_message":"You didn't select a choice.",},)
    else:
         selected_choice.votes=F("votes") + 1
         selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,"polls/results.html",{"question":question})
       