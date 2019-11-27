from collections import defaultdict

from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader


from common.video import get_video_data
from dance.forms import AddStepAppearanceForm, AddStepAppearanceErrorList, GenericErrorList, StepForm, ArtistForm
from .models import Step, StepAppearance, AlternativeStepName, Artist, Video


def index(request):
    context = {}
    return render(request, 'dance/index.html', context)


def list_steps(request):
    steps = Step.objects.all().order_by('-created_at')[:12]
    context = {
        'steps': steps
    }
    template = loader.get_template('dance/step_list.html')
    return HttpResponse(template.render(context, request=request))


def step_creation(request):

    form = StepForm()

    if request.method != 'POST':
        context = {
            'form': form,
        }
        return render(request, 'dance/create_step.html', context)

    form = StepForm(request.POST, error_class=GenericErrorList)
    if form.is_valid():
        creator = form.cleaned_data['creator']
        name = form.cleaned_data['name']
        school = form.cleaned_data['school']

        # TODO: add more security, check for similar steps for creator and similar name

        try:
            with transaction.atomic():
                step = Step.objects.create(name=name, creator=creator, school=school)
                step.save()

            messages.success(request, 'Step created successfully')

        except IntegrityError:
            form.errors['internal'] = "An internal error append, please retry."

    return redirect('dance:step_detail', step_id=step.id)


def step_detail(request, step_id):
    step = get_object_or_404(Step, pk=step_id)

    alternative_names = AlternativeStepName.objects.filter(step__id=step_id).all().order_by('value')
    alternative_name_values = [alternative_name.value for alternative_name in alternative_names]
    list_alternative_names = ', '.join(alternative_name_values)

    videos = defaultdict(list)
    appearances = StepAppearance.objects.filter(step__id=step_id).filter(video__valid=True).all()
    for appearance in appearances:
        videos[appearance.video.type].append({'data': appearance.video, 'time': appearance.time})

    videos.default_factory = None

    context = {
        'step_name': step.name,
        'other_names': list_alternative_names,
        'artist_name': step.creator.name if step.creator else 'unknown artist',
        'school': step.school,
        'videos': videos,
    }

    return render(request, 'dance/step_detail.html', context)


def search_step(request):
    query = request.GET.get('query')

    if not query:
        steps = Step.objects.all()
    else:
        fuzzy_matching_steps = Step.objects.annotate(similarity=TrigramSimilarity('name', query),
                                                     ).filter(similarity__gt=0.3).order_by('-similarity')

        contains_matching_steps = Step.objects.filter(name__icontains=query)

        steps = fuzzy_matching_steps | contains_matching_steps

    title = "Résultats pour la requête %s" % query
    context = {
        'steps': steps,
        'title': title,
    }

    return render(request, 'dance/step_list.html', context)


def step_list(request):
    steps_list = Step.objects.order_by('name')
    paginator = Paginator(steps_list, 50)
    page = request.GET.get('page')

    try:
        steps = paginator.page(page)
    except PageNotAnInteger:
        steps = paginator.page(1)
    except EmptyPage:
        steps = paginator.page(paginator.num_pages)

    context = {
        'steps': steps,
        'paginate': True
    }
    return render(request, 'dance/step_list.html', context)


def artist_creation(request):

    form = ArtistForm()

    if request.method == 'POST':
        form = ArtistForm(request.POST, error_class=GenericErrorList)
        if form.is_valid():
            # TODO: add more security, check for similar artist names

            try:
                with transaction.atomic():
                    artist = form.save()

                messages.success(request, 'Step created successfully')

            except IntegrityError:
                form.errors['internal'] = "An internal error append, please retry."

            return redirect('dance:artist_detail', artist_id=artist.id)

    context = {
        'form': form,
    }
    return render(request, 'dance/create_artist.html', context)


def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    artist_steps = Step.objects.filter(creator__id=artist_id).all().order_by('name')

    context = {
        'artist_name': artist.name,
        'artist_steps': artist_steps,
    }

    return render(request, 'dance/artist_detail.html', context)


def artist_list(request):
    artists_list = Artist.objects.order_by('name')
    paginator = Paginator(artists_list, 50)
    page = request.GET.get('page')

    try:
        artists = paginator.page(page)
    except PageNotAnInteger:
        artists = paginator.page(1)
    except EmptyPage:
        artists = paginator.page(paginator.num_pages)

    context = {
        'artists': artists,
        'paginate': True
    }
    return render(request, 'dance/artist_list.html', context)


def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    if request.method == 'POST':
        form = AddStepAppearanceForm(request.POST, error_class=AddStepAppearanceErrorList)
        if form.is_valid():
            step_id = form.cleaned_data['step']
            minutes = form.cleaned_data['minutes']
            seconds = form.cleaned_data['seconds']
            time = 60 * minutes + seconds

            try:
                with transaction.atomic():
                    stepAppearance = StepAppearance.objects.create(step_id=step_id, video=video, time=time)
                    stepAppearance.save()

                messages.success(request, 'Step added to video successfully')

            except IntegrityError:
                form.errors['internal'] = "An internal error append, please retry."

    appearances = dict()
    step_appearances = StepAppearance.objects.filter(video__id=video_id).all().order_by('time')
    for appearance in step_appearances:
        appearances[appearance.step] = {'creator': appearance.step.creator, 'time': appearance.time}

    form = AddStepAppearanceForm(request.POST, error_class=AddStepAppearanceErrorList)

    context = {
        'video': video,
        'appearances': appearances,
        'form': form,
    }

    return render(request, 'dance/video_detail.html', context)


def video_creation(request):

    if request.method != 'POST':
        return render(request, 'dance/create_video.html')

    video_url = request.POST.get('videoUrl')
    try:
        video = Video.objects.get(url=video_url)
    except Video.DoesNotExist:
        video = None

    if video is None:
        video_data = get_video_data(video_url.strip())

        if video_data:
            video = Video(**video_data)
            video.save()

    # return redirect(reverse('dance:video_detail', args=[video.id]))
    return redirect('dance:video_detail', video_id=video.id)
