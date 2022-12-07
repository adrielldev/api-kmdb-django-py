from django.db import models
from genre.models import Genre

class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length = 10)
    premiere = models.DateField()
    classification = models.IntegerField()
    synopsis = models.TextField()
    genres = models.ManyToManyField(Genre)




