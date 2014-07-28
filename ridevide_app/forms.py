from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

TIME_INPUT_FORMATS = ['%H:%M', '%I:%M%p', '%I:%M %p']

CAMPUS_LOCATION_CHOICES = (('Max P', 'Max P'),
                           ('South', 'South'),
                          )

OFF_CAMPUS_LOCATION_CHOICES = (("O'Hare Airport", "O'Hare Airport"),
                               ('Midway Airport', 'Midway Airport'),
                               ('Millenium Park', 'Millenium Park'),
                               ('Water Tower Place', 'Water Tower Place'),
                               ('Chinatown', 'Chinatown'),
                              )

class AddRideForm(forms.Form):
    date = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       }))
    time = forms.TimeField(
        widget=DateTimePicker(options={#"format": "HH:mm",
                                       "pickDate": False,
                                       }),
        input_formats=TIME_INPUT_FORMATS)

class AddFromCampusRideForm(AddRideForm):
    departure = forms.ChoiceField(
        choices=CAMPUS_LOCATION_CHOICES)
    destination = forms.ChoiceField(
        choices=OFF_CAMPUS_LOCATION_CHOICES)

class AddToCampusRideForm(AddRideForm):
    departure = forms.ChoiceField(
        choices=OFF_CAMPUS_LOCATION_CHOICES)
    destination = forms.ChoiceField(
        choices=CAMPUS_LOCATION_CHOICES)