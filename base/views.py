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

    form = OptionsForm(instance=user_options)

    if request.method == 'POST':
        submit_form = OptionsForm(request.POST, instance=user_options)
        submit_form.save()

        return redirect('/')

    input_fields = (form['step'], form['pairs'], form['starting_bet'])

    column_fields = (form['bet_column'],
                     form['index_column'],
                     form['level_column'],
                     form['net_column'],
                     form['partner_column'],
                     form['play_column'],
                     form['result_column'],
                     form['debt_column'])

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
