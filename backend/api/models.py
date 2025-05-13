from django.db import models
from django.contrib.auth.models import User


class Gym(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_gyms')

    def __str__(self):
        return self.name


class Court(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='courts')
    name = models.CharField(max_length=100)
    game_start_time = models.TimeField()
    game_duration_minutes = models.IntegerField()
    cost_to_join = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} at {self.gym.name}"


class Team(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100)
    max_players = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.name} on {self.court.name}"


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='managers')
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Manager at {self.gym.name}"
