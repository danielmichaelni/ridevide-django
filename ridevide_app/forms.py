from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

TIME_INPUT_FORMATS = ['%H:%M', '%I:%M%p', '%I:%M %p']

CAMPUS_LOCATION_CHOICES = [('Campus', 'Campus'),
                          ]

OFF_CAMPUS_LOCATION_CHOICES = [("O'Hare Airport", "O'Hare Airport"),
                               ('Midway Airport', 'Midway Airport'),
                               ('Union Station', 'Union Station'),
                              ]

ALL_LOCATION_CHOICES = [('All', 'All')] + CAMPUS_LOCATION_CHOICES + OFF_CAMPUS_LOCATION_CHOICES

class AddRideForm(forms.Form):
    date = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                      }))
    time = forms.TimeField(
        widget=DateTimePicker(options={"pickDate": False,
                                      }),
        input_formats=TIME_INPUT_FORMATS)

class AddFromCampusRideForm(AddRideForm):
    #departure = forms.ChoiceField(
    #    choices=CAMPUS_LOCATION_CHOICES)
    departure = 'Campus'
    destination = forms.ChoiceField(
        choices=OFF_CAMPUS_LOCATION_CHOICES)

class AddToCampusRideForm(AddRideForm):
    departure = forms.ChoiceField(
        choices=OFF_CAMPUS_LOCATION_CHOICES)
    #destination = forms.ChoiceField(
    #    choices=CAMPUS_LOCATION_CHOICES)
    destination = 'Campus'

class FilterRidesForm(forms.Form):
    date = forms.DateField(
        required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                      }))
    departure = forms.ChoiceField(
        required=False,
        choices=ALL_LOCATION_CHOICES)
    destination = forms.ChoiceField(
        required=False,
        choices=ALL_LOCATION_CHOICES)
