import os
import random
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from .models import Picture
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


def next_pic(request):
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
    if request.method == 'POST':
        form = UploadPicForm(request.POST, request.FILES)
        if form.is_valid():
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
