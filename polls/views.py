from django.shortcuts import render, get_object_or_404
<<<<<<< HEAD
from django.http import HttpResponse
=======
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
>>>>>>> 57bcc81a0e338b9334b44927bcb42b5650b2c4df

from .models import Question


# Create your views here.

<<<<<<< HEAD
def index(request):
    q_list = Question.objects.order_by('-pub_date')

    context = {
        'q_list': q_list,
    }

    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
=======
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'q_list'

    def get_queryset(self):
        # Returns question list
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "You didn't select a chioce.",
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
>>>>>>> 57bcc81a0e338b9334b44927bcb42b5650b2c4df
