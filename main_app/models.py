from random import choices
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Stuff(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f'A {self.description} {self.name}'
    
    def get_absolute_url(self):
        return reverse('stuffs_detail', kwargs={'pk': self.id})

class Vaca(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    cost = models.CharField(max_length=100)
    stuffs = models.ManyToManyField(Stuff)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('vacas_detail', kwargs={'vaca_id': self.id})

class Traveling(models.Model):
    MOODS = (
        ('B', 'Bad'),
        ('O', 'OK'),
        ('G', 'Good'),
        ('L', 'Loved it'),
    )

    class Meta:
        ordering = ('-date',)

    date = models.DateField('traveling date')
    mood = models.CharField(max_length=1, choices=MOODS, default=MOODS[0][0])
    vaca = models.ForeignKey(Vaca, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_mood_display()} on {self.date}'

class Photo(models.Model):
    url = models.CharField(max_length=200)
    vaca = models.ForeignKey(Vaca, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for vaca_id: {self.vaca_id} @{self.url}'
