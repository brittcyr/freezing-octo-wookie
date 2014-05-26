from django.db import models

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
  team = models.CharField(max_length=40)
  conference = models.CharField(max_length=30)
  number = models.IntegerField(null=True, blank=True)
  year = models.CharField(max_length=7, choices=YEAR_CHOICES)
  height = models.IntegerField(null=True)
  weight = models.IntegerField(null=True)
  home_state = models.CharField(max_length=30)
  def __unicode__(self):
    return self.name



# Game Object
class Game(models.Model):
  away = models.CharField(max_length=40)
  home = models.CharField(max_length=40)
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
  violation = models.BooleanField()
  gb = models.NullBooleanField()		# TRUE is fogo gb, FALSE is no gb
  wing = models.NullBooleanField()		# TRUE is CT or GB from wings
  emo = models.NullBooleanField()
  home_violations = models.IntegerField(null=True)	# Number of violations in the half
  away_violations = models.IntegerField(null=True)	# Number of violations in the half

  def __unicode__(self):
    return self.away + ' vs. ' + self.home + ' @ ' + self.time + ' in the ' + self.quarter + ' quarter of ' + self.game
