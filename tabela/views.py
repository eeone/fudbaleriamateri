from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models import Max

from operator import itemgetter

from .models import Player, Round, Team
from .forms import RoundsForm

class tableEntry():
    name = ''
    wins = 0
    losses = 0
    draws = 0
    points = 0
    played = 0
    pct = 0
    diff = 0

    def __init__(self, wname):
        self.name = wname

def boolToText(b):
    if b == 'True':
        return 'Pobeda'
    else:
        return 'Kita'

def getScore(players, rounds):
    score = list()

    for p in players:
        pTableEntry = tableEntry(p.name)

        for r in rounds:
            if p.id in r.team1.players or p.id in r.team2.players:
                if r.teamWon is None:
                    pTableEntry.draws = pTableEntry.draws + 1
                elif p.id in r.teamWon.players:
                    pTableEntry.wins = pTableEntry.wins + 1
                else:
                    pTableEntry.losses = pTableEntry.losses + 1

        pTableEntry.points =  5 * pTableEntry.wins + 3 * pTableEntry.draws + 1 * pTableEntry.losses
        pTableEntry.played =  pTableEntry.wins + pTableEntry.draws + pTableEntry.losses
        pTableEntry.diff = pTableEntry.wins - pTableEntry.losses

        if pTableEntry.played == 0:
            pTableEntry.pct = 0
        else:
            pTableEntry.pct = round(100 * (pTableEntry.wins + pTableEntry.draws * 0.5) / pTableEntry.played, 2)

            score.append(pTableEntry)

    score = sorted(score, key = lambda x: (x.points, x.name), reverse=True)

    return score

def getRound(r):
    t1 = Team.objects.get(id = r.team1.id)
    t2 = Team.objects.get(id = r.team2.id)

    names = [str(Player.objects.get(id = x)) for x in t1.players] + [str(Player.objects.get(id = x)) for x in t2.players]

    if r.teamWon is None:
        strings = ['Pola' for x in names]
    else:
        bools = [str(x in r.teamWon.players) for x in t1.players] + [str(x in r.teamWon.players) for x in t2.players]
        strings = [boolToText(x) for x in bools]

    return [(x[0], x[1]) for x in list(zip(names, strings))]

# Create your views here.
def index(request):
    currentSeason = Round.objects.latest('date').season
    players = Player.objects.all()
    rounds = Round.objects.filter(season = currentSeason)

    currentRound = [x for x in sorted(rounds, key = lambda y: (y.id), reverse = True)][0]

    roundSelectForm = RoundsForm()

    if request.method == 'POST':
        roundSelectForm = RoundsForm(request.POST)
        currentRound = Round.objects.get(id = request.POST['selectedRound'])

    r = getRound(currentRound)
    score = getScore(players, rounds)

    template = loader.get_template('tabela/index.html')
    context = {
        'score': score,
        'roundSelectForm': roundSelectForm,
        'roundTable': r
    }

    return HttpResponse(template.render(context, request))