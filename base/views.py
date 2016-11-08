from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from base.forms import OptionsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.worker import worker
from multiprocessing import Process, Value
from django import db


user_processes = {}


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

    # sim_status = user_options.simulation_status
    columns = ['name'] + user_options.get_enabled_column_names()

    print("'columns' in simulate() view:", columns)

    context = {
        'columns': columns,
        'start_stop': 'Start'
        # 'start_stop': 'Stop' if sim_status else 'Start'
    }

    return render(request=request,
                  template_name='base/simulate.html',
                  context=context)

@login_required
def start_sim(request, iterations):
    iterations = int(iterations)
    username = request.user.username

    if username in user_processes:
        if user_processes[username].is_alive():
            print('There is already a running process - cannot start sim')
            return HttpResponse('There is already a running process - cannot start sim')

    db.connections.close_all()

    p = Process(target=worker, args=(request.user, iterations))
    p.start()
    user_processes[username] = p
    print('A simulation should be started')

    return HttpResponse('A simulation should be started')


# @login_required
# def stop_sim(request):
#     user_options = request.user.options
#
#     try:
#         user_options.simulation_status = False
#         user_options.save()
#
#         # shared_value = shared_signals[request.user.username]
#         # with shared_value.get_lock():
#         #     print('Sending a stop signal to the process...')
#         #     shared_value.value = 1
#
#         return HttpResponse()
#     except KeyError:
#         return redirect('/simulate')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect('/')

    return render(request=request,
                  template_name='base/login.html')


def sign_out(request):
    logout(request)
    return redirect('/login')