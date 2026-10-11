from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice,Tag
from django.urls import reverse
from django.db.models import F
from django.views import generic

from django.shortcuts import render,get_object_or_404
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        q = (
            Question.objects.filter(pub_date__lte=timezone.now())
            .prefetch_related("tags")
            .order_by("-pub_date")
        )
        tag = self.kwargs.get("tag")
        if tag:
            q = q.filter(tags__name = tag)
        return q
    def get_context_data(self, **kwargs):


        ctx = super().get_context_data(**kwargs)
        ctx["active_tag"] = self.kwargs.get("tag")
        ctx["tags"] = Tag.objects.all()

        return ctx


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request,question_id):
    question = get_object_or_404(Question,pk = question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
       
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "No choice selected",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
       
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    


