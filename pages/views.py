from django.shortcuts import render

from django.http import HttpResponse

from .models import Artist, Step


def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)


def list_steps(request):
    steps = Step.objects.all().order_by('-created_at')[:12]
    steps = ["<li>{}</li>".format(step.name) for step in steps]
    message = """<ul>{}</ul>""".format("\n".join(steps))
    return HttpResponse(message)

