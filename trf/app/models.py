from django.db import models

class Turf(models.Model):
    # Fields for the turf
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateTimeField()
    
    # Choices for games
    CRICKET = 'cricket'
    FOOTBALL = 'football'
    GAME_CHOICES = [
        (CRICKET, 'Cricket'),
        (FOOTBALL, 'Football'),
    ]
    
    # Field for selecting games
    game = models.CharField(
        max_length=10,
        choices=GAME_CHOICES,
        default=CRICKET,  # You can set a default game
    )
    
    def __str__(self):
        return f"{self.name} - {self.get_game_display()}"
