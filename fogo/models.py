from django.db import models

# Team object
class Team(models.Model):
  name = models.CharField(max_length=40)
  # color
  # url
  # logo
  # location
  conference = models.CharField(max_length=60)

  def __unicode__(self):
    return self.name



YEAR_CHOICES = (
  ('FR', 'FR'),
  ('SO', 'SO'),
  ('JR', 'JR'),
  ('SR', 'SR'),
  ('G', 'G'),
  ('UNK', 'UNKNOWN'),
)


# PLAYER Object
class Player(models.Model):
  name = models.CharField(max_length=30)
  team = models.ForeignKey(Team)
  number = models.IntegerField(null=True, blank=True)
  year = models.CharField(max_length=7, choices=YEAR_CHOICES)
  height = models.IntegerField(null=True)
  weight = models.IntegerField(null=True)
  home_state = models.CharField(max_length=30)
  def __unicode__(self):
    return self.name



# Game Object
class Game(models.Model):
  away = models.ForeignKey(Team, related_name='away_team')
  home = models.ForeignKey(Team, related_name='home_team')
  time = models.TimeField()
  date = models.DateField()
  site = models.CharField(max_length=30)
  home_wins = models.IntegerField()
  total_face = models.IntegerField()
  away_score = models.IntegerField()
  home_score = models.IntegerField()

  def __unicode__(self):
    return self.away + ' vs. ' + self.home + ' on ' + str(self.date)



# Ref Object
class Ref(models.Model):
  ref = models.CharField(max_length=30)
  game = models.ForeignKey(Game)

  def __unicode__(self):
    return self.ref + ' @ ' + self.game



# Faceoff object
class Faceoff(models.Model):
  away = models.ForeignKey(Player, related_name='faceoff_away')
  home = models.ForeignKey(Player, related_name='faceoff_home')
  game = models.ForeignKey(Game)
  winner = models.BooleanField()	# TRUE is home, FALSE is away / None
  time = models.TimeField()
  quarter = models.IntegerField()
  reason = models.IntegerField()	# 0 is for start of quarter, 1 for home goal, -1 for away goal
  violation = models.BooleanField()
  gb = models.NullBooleanField()		# TRUE is fogo gb, FALSE is no gb
  wing_gb = models.NullBooleanField()   # TRUE is gb from the wing player
  wing_ct = models.NullBooleanField()   # TRUE is ct by a wing player in next 20 seconds

  def __unicode__(self):
    return self.away + ' vs. ' + self.home + ' @ ' + self.time + ' in the ' + self.quarter + ' quarter of ' + self.game
