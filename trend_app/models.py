from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    location_code = models.TextField()
    location_name = models.TextField()

    def __str__(self) -> str:
        return f"Location: {self.location_code}, {self.location_name}"
class Trend(models.Model):
    trend_name = models.TextField()
    tweet_volume = models.IntegerField()
    day = models.DateField()
    hour = models.TextField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Trend: {self.trend_name}, {self.tweet_volume}"
class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    trend_id = models.ForeignKey(Trend, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Favorite: {self.user_id}, {self.trend_id}"