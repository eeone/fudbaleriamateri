from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    createDate = models.DateTimeField('Create date.')

    def __str__(self):
        return self.name

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    players = ArrayField(models.IntegerField())
    date = models.DateTimeField('Team date.')

    def __str__(self):
        names = ', '.join([str(Player.objects.get(id = x)) for x in self.players]) 
        return str(self.date) + ' ' + names

class Round(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='team2')
    teamWon = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='teamWon')
    date = models.DateTimeField('Date played')

    def __str__(self):
        whoWon = 'Draw'

        if self.teamWon is not None:
            whoWon = self.teamWon

        return 'Season ' + str(self.season) + ', Round ' + str(self.id) + ', Who won: ' + str(whoWon)