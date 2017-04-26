from django.shortcuts import render, redirect, HttpResponse
from . import models
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):

    return render (request, 'login_reg/index.html')
