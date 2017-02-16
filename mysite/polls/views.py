from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,Http404
from django.template import loader
from .models import Question, Choice

########################################################################
########################################################################
# The render() function takes the request object as its first argument, 
# a template name as its second argument and a dictionary as its optional third argument. 
# It returns an HttpResponse object of the given template rendered with the given context.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

#This is an easier way
def index_shortcut(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def index_simple(request):
    return HttpResponse("Hello, world. You're at the polls index.")

########################################################################
########################################################################
#The below method would decouple the model layer from the view layer. 
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def detail_simple(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


#The below method would couple the model layer to the view layer. 
#One of the foremost design goals of Django is to maintain loose coupling.
def detail_main(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    
########################################################################
########################################################################
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def results_sample(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

########################################################################
########################################################################
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def vote_simple(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


