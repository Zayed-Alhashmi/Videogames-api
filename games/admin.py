from django.contrib import admin
from .models import Game, Review

# Registers the Game and Review models so they appear in the Django admin panel
admin.site.register(Game)
admin.site.register(Review)
