from django.db import models

from django.contrib.auth.models import User  # Import User model

class Turf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null temporarily
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateTimeField()

    CRICKET = 'cricket'
    FOOTBALL = 'football'
    GAME_CHOICES = [
        (CRICKET, 'Cricket'),
        (FOOTBALL, 'Football'),
    ]

    game = models.CharField(
        max_length=10,
        choices=GAME_CHOICES,
        default=CRICKET,
    )

    def __str__(self):
        return f"{self.name} - {self.get_game_display()}"

