from django import forms

from .models import Round, Player

class RoundsForm(forms.Form):
    currentSeason = Round.objects.latest('date').season
    rounds = [(str(x.id), str(x.id)) for x in sorted(Round.objects.filter(season = currentSeason), key = lambda y: (y.id), reverse = True)]
    selectedRound = forms.ChoiceField(label='Kolo', widget=forms.Select, choices = rounds)

class JointScoreFormPlayer1(forms.Form):
    currentSeason = Round.objects.latest('date').season
    rounds = Round.objects.filter(season = currentSeason)

    playerIDs = list()
    for r in rounds:
        playerIDs =  playerIDs + r.team1.players + r.team2.players

    playerIDs = list(set(playerIDs))
    players = [Player.objects.get(id = int(x)) for x in playerIDs]
    playerStrings = [(str(x), str(x)) for x in players]

    selectedPlayer1 = forms.ChoiceField(label='Ime', widget=forms.Select, choices = playerStrings)

class JointScoreFormPlayer2(forms.Form):
    currentSeason = Round.objects.latest('date').season
    rounds = Round.objects.filter(season = currentSeason)

    playerIDs = list()
    for r in rounds:
        playerIDs =  playerIDs + r.team1.players + r.team2.players

    playerIDs = list(set(playerIDs))
    players = [Player.objects.get(id = int(x)) for x in playerIDs]
    playerStrings = [(str(x), str(x)) for x in players]

    selectedPlayer2 = forms.ChoiceField(label='Ime', widget=forms.Select, choices = playerStrings)