import os
import random
from django.shortcuts import render
from django.db.models import Count
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Picture, Blocked_Poster, Sms, Blocked_Number, Ad
from .forms import UploadPicForm
from django.contrib.staticfiles.templatetags.staticfiles import static


def _get_pic():
    if Ad.objects.count() > 0 and random.randrange(1, 100) < 10:
        random_index = random.randrange(Ad.objects.count())
        pic = Ad.objects.get(id=random_index)

    # This gives ads from WG Congé an extra chance of showing up. I know it's cheating
    elif Ad.objects.filter(poster='WG Congé')\
            and random.randrange(1, 100) < 20:
        id_list = []
        for ad in Ad.objects.filter(poster='WG Congé'):
            id_list.append(ad.id)

        random_index = random.choice(id_list)
        pic = Ad.objects.get(id=random_index)

    else:
        pic_set = Picture.objects.order_by('-timestamp')[:1]
        if len(pic_set) < 1:
            pic = Picture(url="//lorempixel.com/640/480", poster="lorempixel")
        else:
            pic = pic_set[0]

    return pic


def show_pics(request):
    pic = _get_pic()
    return render(request, "wall/view_pics.html",
                  {'pic': pic,
                   'min_display_time': settings.MIN_DISPLAY_TIME})


def bigscreen(request):
    pic = _get_pic()
    sms_list = Sms.objects.order_by('-timestamp')[:5]
    return render(request, "wall/bigscreen.html",
                  {'pic': pic,
                   'min_display_time': settings.MIN_DISPLAY_TIME,
                   'sms_list': sms_list})


def next_pic(request, current=''):
    if current is '':
        pic = _get_pic()
    else:
        try:
            current_pic = Picture.objects.get(url=current)
            pic = Picture.objects.get(id=current_pic.id + 1)
        except ObjectDoesNotExist:
            pic = _get_pic()

    return JsonResponse({'url': pic.url, 'poster': pic.poster})


def _handle_pic(f):
    filename = str(random.randint(0, 100)) + f.name
    filepath = os.path.join(settings.PIC_STORAGE_LOCATION, filename)
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


def new_pic(request):
    try:
        Blocked_Poster.objects.get(
            ip=request.META.get('REMOTE_ADDR'))
        # this only happens if there is such a poster
        return render(request, 'wall/blocked.html',
                      {'passive_agressive': settings.PASSIVE_AGRESSIVE})
    except ObjectDoesNotExist:
        # We're all fine here. Still need to test the username though
        pass

    if request.method == 'POST':
        form = UploadPicForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Blocked_Poster.objects.get(name=request.POST['poster'].lower())
                return render(request,
                              'wall/blocked.html',
                              {'passive_agressive': settings.PASSIVE_AGRESSIVE})
            except ObjectDoesNotExist:
                pass

            filename = _handle_pic(request.FILES['file'])
            Picture.objects.create(poster=request.POST['poster'],
                                   url=static("pics/" + filename),
                                   ip=request.META.get('REMOTE_ADDR'))
            return HttpResponseRedirect(reverse('show_pics'))
        else:
            form = UploadPicForm()
            return render(request, 'wall/upload.html', {'form': form})
    else:
        form = UploadPicForm()
        return render(request, 'wall/upload.html', {'form': form})


def incoming_sms(request):
    phone = request.GET.get('phone')
    text = request.GET.get('text')

    if phone is None or text is None:
        return HttpResponse('')
    else:
        try:
            Blocked_Number.objects.get(number=phone)
            return HttpResponse('')
        except ObjectDoesNotExist:
            pass
        Sms.objects.create(sender=phone, text=text)
        return HttpResponse('')


def get_sms(request):
    sms_list = Sms.objects.order_by('-timestamp')[:5]
    return render(request, "wall/sms.html", {'sms_list': sms_list})


def leaderboard(request):
    # This gets all unique "sender" values,
    # annotates them with their count by primary key,
    # and orders them large to small by that count. We only need the first 10
    sms_leaders = Sms.objects.values('sender')\
                             .annotate(n=Count('pk'))\
                             .order_by('-n')[:10]
    pic_leaders = Picture.objects.values('poster')\
                                 .annotate(n=Count('pk'))\
                                 .order_by('-n')[:10]
    return render(request, 'wall/leaderboard.html',
                  {'sms_leaders': sms_leaders, 'pic_leaders': pic_leaders})
