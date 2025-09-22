# timetable/forms.py
from django import forms
from .models import TimeTable

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        time_slot = cleaned_data.get('time_slot')
        room = cleaned_data.get('room')

        # Check for conflicts
        if TimeTable.objects.filter(day=day, time_slot=time_slot, room=room).exists():
            raise forms.ValidationError("Room is already booked for this time slot!")

        return cleaned_data
