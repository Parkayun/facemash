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

    def get_all_summoner_data(self):
        data = Warrior.objects.filter(fb_id=self.fb_id)
        data_len = len(data)
        return {
            'score': data.aggregate(models.Sum('score'))['score__sum'] / data_len,
            'wins':  data.aggregate(models.Sum('wins'))['wins__sum'],
            'losses': data.aggregate(models.Sum('losses'))['losses__sum'] 
        }

    def get_performance(self):
        data = Warrior.objects.filter(fb_id=self.fb_id)
        wins = data.aggregate(models.Sum('wins'))['wins__sum']
        losses = data.aggregate(models.Sum('losses'))['losses__sum']
        try:
            return self.score / (1 + (losses / wins))
        except ZeroDivisionError:
            return 0


class Battle(models.Model):
    winner = models.ForeignKey(Warrior, related_name='winner')
    loser = models.ForeignKey(Warrior, related_name='loser')
    summoner = models.ForeignKey(Profile, related_name='summoner')
    created_at = models.DateTimeField(auto_now_add=True)
