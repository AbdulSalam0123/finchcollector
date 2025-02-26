from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS =(
    (
        'B', 'Breakfast'
    ),
    (
        'L', 'Lunch'
    ),
    (
        'D', 'Dinner'
    )
)

# Create your models here.

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})



class Finch(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    age = models.IntegerField()
    # image = models.CharField(default=None, blank=True, null=True, max_length=2000)
    image = models.ImageField(upload_to="finches/static/uploads/", default="")
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})
    def __str__(self):
        return self.name
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    
class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.finch.name} {self.get_meal_display()} on {self.date} '
    
