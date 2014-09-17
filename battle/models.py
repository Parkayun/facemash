# -*- coding:utf-8 -*-
from django.db import models

from django_facebook.models import FacebookProfile as Profile


class Warrior(models.Model):
    summoner = models.ForeignKey(Profile)
    fb_id = models.CharField(unique=True, max_length=50)
    fb_image_url = models.URLField()
    score = models.IntegerField(default=1500)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class RawWarrior(models.Model):
    summoner = models.ForeignKey(Profile)
    raw = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Battle(models.Model):
    winner = models.ForeignKey(Warrior, related_name='winner')
    loser = models.ForeignKey(Warrior, related_name='loser')
    created_at = models.DateTimeField(auto_now_add=True)
