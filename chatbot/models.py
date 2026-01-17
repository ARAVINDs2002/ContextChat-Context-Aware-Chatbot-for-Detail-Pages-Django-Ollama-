from django.db import models

class House(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('medical', 'Medical'),
        ('school', 'School'),
        ('transportation', 'Transportation'),
        ('shopping', 'Shopping'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class HouseDistance(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='distances')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    distance_in_meters = models.IntegerField()

    def __str__(self):
        return f"{self.place.name} is {self.distance_in_meters}m from {self.house.name}"
