from django.shortcuts import render, redirect
from django.http import HttpResponse
from base.models import Options
from django.contrib.auth.models import User


def home_page(request):
    return render(request, 'base/home.html')


def play_page(request):
    return render(request, 'base/play.html',
                  {'new_item_text': 'A new table item'})


def options(request):
    if request.method == 'POST':
        user = User.objects.get(username='john')
        user_options = Options(user=user)

        current_user = User.objects.get(username='john')
        user_options.user = current_user

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

    columns = ['Bet', 'Index', 'Level', 'Net', 'Partner', 'Play', 'Result', 'Debt']
    inputs = {'starting_bet':
                  {'name': 'Starting bet',
                   'min': 0.1,
                   'max': 100,
                   'step': 0.1,
                   'default': 1
                   },
              'step':
                  {'name': 'Step',
                   'min': 2,
                   'max': 5,
                   'step': 1,
                   'default': 2
                   },
              'pairs':
                  {'name': 'Pairs',
                   'min': 1,
                   'max': 50,
                   'step': 1,
                   'default': 1
                   }
              }

    return render(request, 'base/options.html', context={
        'columns': columns,
        'inputs': inputs
    })
