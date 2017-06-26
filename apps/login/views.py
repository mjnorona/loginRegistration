
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def index(request):
    list = User.userManager.all()
    for i in list:
        print i.email
    return render(request, 'login/index.html')


def register(request):

    if request.method == "POST":
        values = User.userManager.register(request.POST['first'], request.POST['last'], request.POST['email'], request.POST['password'], request.POST['confirm'])
        successful = True

        if values[0]:
            if not values[1]:
                messages.error(request, 'First Name can only contain letters and must have at least 2 characters')
                successful = False
            if not values[2]:
                messages.error(request, 'Last Name can only contain letters and must have at least 2 characters')
                successful = False
            if not values[3]:
                messages.error(request, 'Email is not valid')
                successful = False
            if not values[4]:
                messages.error(request, 'Password must be at least 8 characters')
                successful = False
            if not values[5]:
                messages.error(request, 'Passwords do not match')
                successful = False

            if successful:

                User.userManager.create(first_name=request.POST['first'], last_name=request.POST['last'],
                                        email=request.POST['email'], password=request.POST['password'])
                request.session['name'] = request.POST['first']
                return redirect('/success')
            else:
                return redirect('/')
        else:
            messages.error(request, 'User with email already exists')
            return redirect('/')


def login(request):
    if request.method == "POST":
        login = User.userManager.login(request.POST['email'], request.POST['password'])
        print login
        if login[0]:
            request.session['name'] = login[1]
            return redirect('/success')
        else:
            messages.error(request, 'Email or password is incorrect')
            return redirect('/')

def success(request):
    content = {'name' : request.session['name']}
    return render(request, 'login/success.html', content)