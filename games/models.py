from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    release_year = models.IntegerField(null=True, blank=True)
    developer = models.CharField(max_length=200, null=True, blank=True)
    critic_score = models.FloatField(null=True, blank=True)
    age_rating = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.reviewer_name} - {self.game.title}"
