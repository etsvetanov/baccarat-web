from django.shortcuts import render, redirect
from base.forms import OptionsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def home_page(request):
    return render(request, 'base/home.html')


@login_required
def play_page(request):
    return render(request, 'base/play.html',
                  {'new_item_text': 'A new table item'})

@login_required
def options(request):
    user_options = request.user.options

    if request.method == 'POST':
        submit_form = OptionsForm(request.POST, instance=user_options)
        submit_form.save()

        return redirect('/')

    form = OptionsForm(instance=user_options)

    return render(request=request,
                  template_name='base/options.html',
                  context={
                      'input_fields': form.input_fields,
                      'column_fields': form.columns,
                      'row_fields': form.rows,
                  })


@login_required
def simulate(request):
    user_options = request.user.options

    columns = ['name'] + user_options.get_enabled_column_names()
    print("'columns' in simulate() view:", columns)

    context = {
        'columns': columns
    }

    return render(request=request,
                  template_name='base/simulate.html',
                  context=context)


def sign_in(request):
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


def sign_out(request):
    logout(request)
    return redirect('/login')