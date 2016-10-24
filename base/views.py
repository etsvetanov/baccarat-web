from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import IntegerField, BooleanField
from base.models import Options
from base.forms import OptionsForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms import TextInput


def home_page(request):
    return render(request, 'base/home.html')


def play_page(request):
    return render(request, 'base/play.html',
                  {'new_item_text': 'A new table item'})


def options(request):
    user_options = request.user.options

    if request.method == 'POST':
        submit_form = OptionsForm(request.POST, instance=user_options)
        submit_form.save()

        return redirect('/')

    form = OptionsForm(instance=user_options)
    input_fields = (form['step'], form['pairs'], form['starting_bet'])

    # column_fields = (form['bet_column'],
    #                  form['index_column'],
    #                  form['level_column'],
    #                  form['net_column'],
    #                  form['partner_column'],
    #                  form['choice_column'],
    #                  form['result_column'],
    #                  form['debt_column'])

    column_fields = form.columns

    row_fields = (form['virtual_player_rows'], form['real_player_rows'])

    return render(request=request,
                  template_name='base/options.html',
                  context={
                      'input_fields': input_fields,
                      'column_fields': column_fields,
                      'row_fields': row_fields,
                      'form': form,
                      'input_field': IntegerField,
                      'check_box_field': BooleanField
                  })


def simulate(request):
    user_options = request.user.options

    columns = user_options.get_enabled_column_names()
    print("'columns' in simulate() view:", columns)

    context = {
        'columns': columns
    }

    return render(request=request,
                  template_name='base/simulate.html',
                  context=context)

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print('user is not None')
            login(request=request, user=user)
            return redirect('/')
        else:
            print("NOOOOOOOOOOOOOO")
    return render(request=request,
                  template_name='base/login.html')