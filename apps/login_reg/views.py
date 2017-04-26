from django.shortcuts import render, redirect, HttpResponse
from .models import Users
from . import models
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    try:
        del request.session['logged_id']
    except:
        pass 
    if request.method == "POST":
        try:
            request.session.pop['logged_id']
        except:
            pass
    if not 'errors' in request.session:
        request.session['errors'] = []
    return render (request, 'login_reg/index.html')

def login(request):
    if request.method == "POST":
        result = Users.usermanager.loginValid(request.POST['email'],request.POST['password'])
        print result[1]
        if result[0]:
            request.session['first_name'] = result[1].first_name
            request.session['logged_id'] = result[1].id
            try:
                request.session.pop('errors')
            except KeyError:
                pass
            return redirect(reverse('travels:index'))
        else:
            request.session['errors'] = result[1]
            return redirect(reverse('login_reg:index'))
    else:
        return redirect(reverse('login_reg:index'))

def create(request):
    if request.method == "POST":
        result = Users.usermanager.registerValid(request.POST['first_name'], request.POST['last_name'],request.POST['email'], request.POST['password'], request.POST['conf_pw'])
        if result[0]:
            request.session['first_name'] = result[1].first_name
            request.session['logged_id'] = result[1].id
            try:
                request.session.pop('errors')
            except:
                pass
            return redirect(reverse('travels:index'))
        else:
            request.session['errors'] = result[1]
            return redirect(reverse('login_reg:index'))
    else:
        return redirect(reverse('login_reg:index'))

def success(request):

    return render (request, 'login_reg/success.html', {'first_name': request.session.get('first_name')})
