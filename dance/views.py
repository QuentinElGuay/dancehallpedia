from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader

from .models import Step, StepAppearance


def index(request):
    context = {}
    return render(request, 'dance/index.html', context)


def list_steps(request):
    steps = Step.objects.all().order_by('-created_at')[:12]
    context = {
        'steps': steps
    }
    template = loader.get_template('dance/list_steps.html')
    return HttpResponse(template.render(context, request=request))


def detail(request, step_id):
    step = get_object_or_404(Step, pk=step_id)

    videos = defaultdict(list)

    appearances = StepAppearance.objects.filter(step__id=step_id).filter(video__valid=True).all()
    for appearance in appearances:
        videos[appearance.video.type].append({'data': appearance.video, 'time': appearance.time})

    videos.default_factory = None

    context = {
        'step_name': step.name,
        'artist_name': step.creator.name,
        'school': step.school,
        'videos': videos,
    }

    return render(request, 'dance/step_detail.html', context)
