from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import Users

# Create your models here.
class UserManager(models.Manager):
    def add_user_to_trip(self, name, description, travel_start, travel_end, logged_id):
        errors = []
        if len(name) == 0:
            errors.append("Name is required")
        elif len(description) == 0:
            errors.append("Description  is required")
        elif Locations.usermanager.filter(name=name):
            errors.append("This Trip is already planned")
        if len(errors) is not 0:
            return (False, errors)
        else:
            t = Locations(name=name, description=description, travel_start=travel_start, travel_end=travel_end)
            t.save()
            print t.id
            trip = Locations.usermanager.get(id=t.id)
            user = Users.usermanager.get(id=logged_id)
            trip.travel_id.add(user)
            trip.planner_id = user
            trip.save()
            return (True, t)

    def join_user_to_trip(self, logged_id, place_id):
        t = Locations.usermanager.get(id=place_id)
        u = Users.usermanager.get(id=logged_id)
        t.travel_id.add(u)
        print t.travel_id
        return (True, t)



class Locations(models.Model):
    travel_id = models.ManyToManyField(Users, related_name='usertotrip')
    planner_id = models.ForeignKey(Users, related_name='usertoplanner', null=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    travel_start = models.DateField(blank=True, null=True)
    travel_end = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    usermanager = UserManager()
