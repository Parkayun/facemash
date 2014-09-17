# -*- coding:utf-8 -*-
from django.db import models


class Warrior(models.Model):
    fb_id = models.CharField(unique=True, max_length=50)
    fb_image_url = models.URLField()
    score = models.IntegerField(default=1500)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)


class Battle(models.Model):
    winner = models.ForeignKey(Warrior)
    loser = models.ForeignKey(Warrior)
