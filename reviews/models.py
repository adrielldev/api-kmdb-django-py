from django.db import models
from users.models import User
from movies.models import Movie
from django.core.validators import MaxValueValidator, MinValueValidator 



class Review(models.Model):
    RECOMENDATIONS = [
        ('Must Watch','Must Watch'),
        ('Should Watch','Should Watch'),
        ('Avoid Watch','Avoid Watch'),
        ('No Opinion','No Opinion'),
    ]
    stars = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(10)])
    review = models.TextField()
    spoilers = models.BooleanField()
    recomendation = models.CharField(max_length=50,choices=RECOMENDATIONS,default='No Opinion')
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete = models.CASCADE)
