from django import forms

from .models import Round

class RoundsForm(forms.Form):
    currentSeason = Round.objects.latest('date').season
    rounds = [(str(x.id), str(x.id)) for x in sorted(Round.objects.filter(season = currentSeason), key = lambda y: (y.id), reverse = True)]
    selectedRound = forms.ChoiceField(label='Kolo', widget=forms.Select, choices = rounds)