from django.shortcuts import render, redirect
from django.http import HttpResponse
from base.models import Options


def home_page(request):
    return render(request, 'base/home.html')


def play_page(request):
    return render(request, 'base/play.html',
                  {'new_item_text': 'A new table item'})


def options(request):
    if request.method == 'POST':
        user_options = Options()
        for attr in Options.OPTION_FIELDS:
            if attr not in request.POST:
                setattr(user_options, attr, False)
            else:
                value = request.POST[attr]
                if value == 'on':
                    value = True
                setattr(user_options, attr, value)

        user_options.save()

        return redirect('/')

    return render(request, 'base/options.html')
