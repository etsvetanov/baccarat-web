from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import IntegerField, BooleanField
from base.models import Options
from base.forms import OptionsForm
from django.contrib.auth.models import User
from django.forms import TextInput


def home_page(request):
    return render(request, 'base/home.html')


def play_page(request):
    return render(request, 'base/play.html',
                  {'new_item_text': 'A new table item'})


def options(request):
    current_user = User.objects.get(username='john')

    try:
        user_options = Options.objects.get(user=current_user)
    except Options.DoesNotExist:
        user_options = Options(user=current_user)
        user_options.save()

    form = OptionsForm()

    if request.method == 'POST':

        # for attr in Options.OPTION_FIELDS:
        #     if attr not in request.POST:
        #         setattr(user_options, attr, False)
        #     else:
        #         value = request.POST[attr]
        #         if value == 'on':
        #             value = True
        #         setattr(user_options, attr, value)

        user_options.save()

        return redirect('/')

    input_fields = (form['step'], form['pairs'], form['starting_bet'])
    checkbox_fields = (form['bet_column'],
                       form['index_column'],
                       form['level_column'],
                       form['net_column'],
                       form['partner_column'],
                       form['play_column'],
                       form['result_column'],
                       form['debt_column'])

    return render(request=request,
                  template_name='base/options.html',
                  context={
                      'input_fields': input_fields,
                      'checkbox_fields': checkbox_fields,
                      'form': form,
                      'input_field': IntegerField,
                      'check_box_field': BooleanField
                  })
    # columns = ['Bet', 'Index', 'Level', 'Net', 'Partner', 'Play', 'Result', 'Debt']
    #
    # inputs = {'starting_bet':
    #               {'name': 'Starting bet',
    #                'min': 0.1,
    #                'max': 100,
    #                'step': 0.1,
    #                'default': 1
    #                },
    #           'step':
    #               {'name': 'Step',
    #                'min': 2,
    #                'max': 5,
    #                'step': 1,
    #                'default': 2
    #                },
    #           'pairs':
    #               {'name': 'Pairs',
    #                'min': 1,
    #                'max': 50,
    #                'step': 1,
    #                'default': 1
    #                }
    #           }
    #
    # return render(request, 'base/options.html', context={
    #     'columns': columns,
    #     'inputs': inputs
    # })
