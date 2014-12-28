from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ridevide_app import forms
from ridevide_app.models import Ride, UserProfile
import datetime
import itertools

### Helper Methods

def outsideTimeBan(time1, time2, constraint_minutes):
    d = datetime.date.today()
    dt1 = datetime.datetime.combine(d, time1)
    dt2 = datetime.datetime.combine(d, time2)
    if abs((dt1 - dt2).total_seconds()) > (constraint_minutes * 60):
        return True
    return False

# disallow users to sign up for two or more rides that are less than 30 minutes apart
def eligibleForRide(request, date, time):
    check_rides = request.user.profile.ride_set.filter(date=date);
    for ride in check_rides:
        if not outsideTimeBan(ride.time, time, 30):
            return False
    return True

### Views

def index(request):
    if request.user.is_authenticated():
        today = datetime.date.today().strftime('%Y-%m-%d')
        my_rides = request.user.profile.ride_set.filter(date__gte=today).order_by('date')
        if my_rides.count() == 0:
            return render(request, "ridevide_app/index.html")
        else:
            return browse_rides(request, my_rides, "My Upcoming Rides")
    else:
        return render(request, "ridevide_app/landing.html")

@login_required(login_url='/')
def browse(request):
    return render(request, "ridevide_app/browse.html")

@login_required(login_url='/')
def browse_detail(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    today = datetime.date.today()
    if ride.date < today:
        archived = True
    else:
        archived = False
    return render(request, "ridevide_app/browse_detail.html", dict(ride=ride, ride_id=ride_id, archived=archived))

@login_required(login_url='/')
def add_user_to_ride(request, ride_id):
    error = ''
    ride = get_object_or_404(Ride, pk=ride_id)
    if request.method == 'POST':
        if eligibleForRide(request, ride.date, ride.time):
            ride.riders.add(request.user.profile)
        else:
            error = 'Cannot join multiple rides within 30 minutes of each other. Remove yourself from the conflicting ride in order to join this ride.'
            return render(request, "ridevide_app/browse_detail.html", dict(ride=ride, ride_id=ride_id, error=error))
    return redirect("/browse/%d" % int(ride_id))

@login_required(login_url='/')
def delete_user_from_ride(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    if request.method == 'POST':
        ride.riders.remove(request.user.profile)
        if ride.riders.count() == 0:
            ride.delete()
            return redirect("/")
    return redirect("/browse/%d" % int(ride_id))

def browse_rides(request, rides, heading):
    formatted_rides = []
    for k, g in itertools.groupby(rides, lambda x: x.date):
        tmp_rides = []
        for ride in sorted(list(g), key = lambda r: r.time):
            tmp_rides.append(ride)
        formatted_rides.append(tmp_rides)
    return render(request, "ridevide_app/browse_rides.html", dict(heading=heading, formatted_rides=formatted_rides))

@login_required(login_url='/')
def browse_from_campus(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    from_campus_rides = Ride.objects.filter(from_campus=True, date__gte=today).order_by('date')
    return browse_rides(request, from_campus_rides, "Browse Rides from Campus")

@login_required(login_url='/')
def browse_to_campus(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    to_campus_rides = Ride.objects.filter(from_campus=False, date__gte=today).order_by('date')
    return browse_rides(request, to_campus_rides, "Browse Rides to Campus")

@login_required(login_url='/')
def search(request):
    if request.method == 'POST':
        form = forms.FilterRidesForm(request.POST)
        if form.is_valid():
            rides = Ride.objects.order_by('date')
            date = form.cleaned_data['date']
            departure = form.cleaned_data['departure']
            destination = form.cleaned_data['destination']
            if date:
                rides = rides.filter(date=date)
            if departure != "All":
                rides = rides.filter(departure=departure)
            if destination != "All":
                rides = rides.filter(destination=destination)
            return browse_rides(request, rides, "Search Results")
    else:
        form = forms.FilterRidesForm()
        return render(request, "ridevide_app/search.html", dict(form=form))

@login_required(login_url='/')
def add(request):
    return render(request, "ridevide_app/add.html")

@login_required(login_url='/')
def add_from_campus(request):
    if request.method == 'POST':
        form = forms.AddFromCampusRideForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            departure = 'Campus' #form.cleaned_data['departure']
            destination = form.cleaned_data['destination']
            today = datetime.date.today()
            if date < today:
                error = 'Cannot enter a date in the past.'
                return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride from Campus", error=error))
            if eligibleForRide(request, date, time):
                r = Ride(date=date, time=time, departure=departure, destination=destination, from_campus=True)
                r.save()
                profile = request.user.profile
                r.riders.add(profile)
                return redirect("/browse/%d" % r.id)
            else:
                error = 'Cannot be in multiple rides within 30 minutes of each other. Remove yourself from the conflicting ride in order to create this ride.'
                return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride from Campus", error=error))
        else:
            return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride from Campus"))
    else:
        form = forms.AddFromCampusRideForm()
        return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride from Campus"))

@login_required(login_url='/')
def add_to_campus(request):
    if request.method == 'POST':
        form = forms.AddToCampusRideForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            departure = form.cleaned_data['departure']
            destination = 'Campus' #form.cleaned_data['destination']
            today = datetime.date.today()
            if date < today:
                error = 'Cannot enter a date in the past.'
                return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride from Campus", error=error))
            if eligibleForRide(request, date, time):
                r = Ride(date=date, time=time, departure=departure, destination=destination, from_campus=False)
                r.save()
                profile = request.user.profile
                r.riders.add(profile)
                return redirect("/browse/%d" % r.id)
            else:
                error = 'Cannot be in multiple rides within 30 minutes of each other. Remove yourself from the conflicting ride in order to create this ride.'
                return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride to Campus", error=error))
        else:
            return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride to Campus"))
    else:
        form = forms.AddToCampusRideForm()
        return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride to Campus"))

@login_required(login_url='/')
def contact(request):
    return render(request, "ridevide_app/contact.html")

def stats(request):
    total_rides = Ride.objects.all()
    today = datetime.date.today()
    completed_rides = total_rides.filter(date__lt=today)
    completed_rides_with_2_riders = 0
    completed_rides_with_3_riders = 0
    completed_rides_with_4_riders = 0
    for completed_ride in completed_rides:
        num_riders = len(completed_ride.riders.all())
        if num_riders == 2:
            completed_rides_with_2_riders += 1
        if num_riders == 3:
            completed_rides_with_3_riders += 1
        if num_riders == 4:
            completed_rides_with_4_riders += 1
    completed_rides_with_more_than_2_riders = completed_rides_with_2_riders + completed_rides_with_3_riders + completed_rides_with_4_riders
    completed_rides_with_more_than_3_riders = completed_rides_with_3_riders + completed_rides_with_4_riders
    upcoming_rides = total_rides.filter(date__gte=today)
    users = UserProfile.objects.all()
    return render(request, "ridevide_app/stats.html", dict(total_rides=total_rides, completed_rides=completed_rides, upcoming_rides=upcoming_rides, users=users, completed_rides_with_more_than_2_riders=completed_rides_with_more_than_2_riders, completed_rides_with_more_than_3_riders=completed_rides_with_more_than_3_riders, completed_rides_with_4_riders=completed_rides_with_4_riders))

@login_required(login_url='/')
def archives(request):
    rides = Ride.objects.order_by('date')
    return browse_rides(request, rides, "Archived Rides")