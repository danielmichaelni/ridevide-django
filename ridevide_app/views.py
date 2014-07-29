from django.shortcuts import render, redirect, get_object_or_404
from ridevide_app import forms
from ridevide_app.models import Ride
import datetime
import itertools

def index(request):
    if request.user.is_authenticated():
        if request.user.profile.ride_set.count() == 0:
            return render(request, "ridevide_app/index.html")
        else:
            my_rides = request.user.profile.ride_set.order_by('date')
            return browse_rides(request, my_rides, "My Upcoming Rides")
    else:
        return render(request, "ridevide_app/landing.html")

def browse(request):
    if request.user.is_authenticated():
        return render(request, "ridevide_app/browse.html")
    else:
        return redirect("/")

def browse_detail(request, ride_id):
    if request.user.is_authenticated():
        ride = get_object_or_404(Ride, pk=ride_id)
        return render(request, "ridevide_app/browse_detail.html", dict(ride=ride, ride_id=ride_id))
    else:
        return redirect("/")

def add_user_to_ride(request, ride_id):
    if request.user.is_authenticated():
        ride = get_object_or_404(Ride, pk=ride_id)
        if request.method == 'POST':
            ride.riders.add(request.user.profile)
        return redirect("/browse/%d" % int(ride_id))
    else:
        return redirect("/")

def delete_user_from_ride(request, ride_id):
    if request.user.is_authenticated():
        ride = get_object_or_404(Ride, pk=ride_id)
        if request.method == 'POST':
            ride.riders.remove(request.user.profile)
            if ride.riders.count() == 0:
                ride.delete()
                return redirect("/")
        return redirect("/browse/%d" % int(ride_id))
    else:
        return redirect("/")

def browse_rides(request, rides, heading):
    formatted_rides = []
    for k, g in itertools.groupby(rides, lambda x: x.date):
        tmp_rides = []
        for ride in sorted(list(g), key = lambda r: r.time):
            tmp_rides.append(ride)
        formatted_rides.append(tmp_rides)
    return render(request, "ridevide_app/browse_rides.html", dict(heading=heading, formatted_rides=formatted_rides))

def browse_from_campus(request):
    if request.user.is_authenticated():
        today = datetime.date.today().strftime('%Y-%m-%d')
        Ride.objects.filter(date__lt=today).delete()
        from_campus_rides = Ride.objects.filter(from_campus=True).order_by('date')
        return browse_rides(request, from_campus_rides, "Browse Rides from Campus")
    else:
        return redirect("/")

def browse_to_campus(request):
    if request.user.is_authenticated():
        today = datetime.date.today().strftime('%Y-%m-%d')
        Ride.objects.filter(date__lt=today).delete()
        to_campus_rides = Ride.objects.filter(from_campus=False).order_by('date')
        return browse_rides(request, to_campus_rides, "Browse Rides to Campus")
    else:
        return redirect("/")

def search(request):
    if request.user.is_authenticated():
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
    else:
        return redirect("/")

def add(request):
    if request.user.is_authenticated():
        return render(request, "ridevide_app/add.html")
    else:
        return redirect("/")

def add_from_campus(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.AddFromCampusRideForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                departure = form.cleaned_data['departure']
                destination = form.cleaned_data['destination']
                r = Ride(date=date, time=time, departure=departure, destination=destination, from_campus=True)
                r.save()
                profile = request.user.profile
                r.riders.add(profile)
                return redirect("/browse/%d" % r.id)
        else:
            form = forms.AddFromCampusRideForm()
            return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride from Campus"))
    else:
        return redirect("/")

def add_to_campus(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.AddToCampusRideForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                departure = form.cleaned_data['departure']
                destination = form.cleaned_data['destination']
                r = Ride(date=date, time=time, departure=departure, destination=destination, from_campus=False)
                r.save()
                profile = request.user.profile
                r.riders.add(profile)
                return redirect("/browse/%d" % r.id)
        else:
            form = forms.AddToCampusRideForm()
            return render(request, "ridevide_app/add_rides.html", dict(form=form, heading="Add Ride to Campus"))
    else:
        return redirect("/")