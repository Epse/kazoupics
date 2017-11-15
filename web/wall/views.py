import os
import random
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Picture, Blocked_Poster
from .forms import UploadPicForm
from django.contrib.staticfiles.templatetags.staticfiles import static


def _get_pic():
    pic_set = Picture.objects.order_by('-timestamp')[:1]
    if len(pic_set) < 1:
        pic = Picture(url="//lorempixel.com/640/480", poster="lorempixel")
    else:
        pic = pic_set[0]

    return pic

def show_pics(request):
    pic = _get_pic()
    return render(request, "wall/view_pics.html", {'pic': pic, 'bigscreen': False})

def bigscreen(request):
    pic = _get_pic()
    return render(request, "wall/view_pics.html", {'pic': pic, 'bigscreen': True})


def next_pic(request, current=''):
    if current is '':
        pic = _get_pic()
    else:
        try:
            current_pic = Picture.objects.get(url=current)
            pic = Picture.objects.get(id=current_pic.id + 1)
        except ObjectDoesNotExist:
            pic = _get_pic()

    return JsonResponse({ 'url': pic.url, 'poster': pic.poster })


def _handle_pic(f):
    filename = str(random.randint(0, 100)) + f.name
    filepath = os.path.join(settings.BASE_DIR, "static", "pics", filename)
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


def new_pic(request):
    try:
        blocked_poster = Blocked_Poster.objects.get(ip=request.META.get('REMOTE_ADDR'))
        # this only happens if there is such a poster
        return render(request, 'wall/blocked.html', {'passive_agressive': settings.PASSIVE_AGRESSIVE})
    except ObjectDoesNotExist:
        # We're all fine here. Still need to test the username though
        pass

    if request.method == 'POST':
        form = UploadPicForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                blocked_poster = Blocked_Poster.objects.get(name=request.POST['poster'])
                return render(request, 'wall/blocked.html', {'passive_agressive': settings.PASSIVE_AGRESSIVE})
            except ObjectDoesNotExist:
                pass

            filename = _handle_pic(request.FILES['file'])
            Picture.objects.create(poster=request.POST['poster'], url=static("pics/" + filename), ip=request.META.get('REMOTE_ADDR'))
            print(static(filename))
            return HttpResponseRedirect(reverse('show_pics'))
        else:
            form = UploadPicForm()
            return render(request, 'wall/upload.html', {'form': form})
    else:
        form = UploadPicForm()
        return render(request, 'wall/upload.html', {'form': form})
