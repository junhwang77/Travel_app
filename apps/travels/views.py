from django.shortcuts import render, redirect, HttpResponse
from .models import Locations
from . import models
from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    schedules = Locations.usermanager.filter(travel_id=request.session['logged_id'])
    others = Locations.usermanager.exclude(planner_id=request.session['logged_id']).exclude(travel_id=request.session['logged_id'])
    context={
        'schedules':schedules,
        'others':others,
    }
    return render(request, 'travels/index.html', context)

def destination(request, id):
    logged_id = request.session['logged_id']
    destination = Locations.usermanager.get(id=id)
    planner = Locations.usermanager.filter(planner_id=id)
    other_users = Locations.usermanager.filter(id=id)
    context = {
        'name':destination.name,
        'first_name':destination.planner_id.first_name,
        'last_name':destination.planner_id.last_name,
        'description':destination.description,
        'start':destination.travel_start,
        'end':destination.travel_end,
        'other_users':other_users
    }
    return render(request, 'travels/destination.html', context)

def add(request):
    if request.method == 'POST':
        request.session['logged_id'] = request.POST['logged_id']
        try:
            request.session.pop('errors')
        except:
            pass
    return render(request, 'travels/add.html')

def create(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
        result = Locations.usermanager.add_user_to_trip(request.POST['name'], request.POST['description'], request.POST['travel_start'], request.POST['travel_end'], request.POST['logged_id'])
        if result[0]:
            try:
                request.session.pop('errors')
            except:
                pass
            return redirect(reverse('travels:index'))
        else:
            request.session['errors'] = result[1]
        return redirect(reverse('travels:add'))
    else:
        return redirect(reverse('travels:add'))

def join(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
        result =  Locations.usermanager.join_user_to_trip(request.POST['logged_id'], request.POST['place_id'])
        return redirect(reverse('travels:index'))

def remove(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
        logged_id = request.POST['logged_id']
        planner_id = request.POST['planner_id']
        t = Locations.usermanager.get(id=request.POST['place_id'])
        if planner_id != logged_id:
            t.travel_id.remove(logged_id)
        else:
            t.delete()
        return redirect(reverse('travels:index'))
