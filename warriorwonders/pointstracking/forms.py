from django import forms

class UpdatePointsForm(forms.Form):
    points = forms.IntegerField(label='Points')