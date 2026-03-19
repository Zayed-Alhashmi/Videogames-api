from rest_framework import serializers
from .models import Game, Review

# Converts Review model instances to and from JSON for use in the API
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# Converts Game model instances to and from JSON, and nests all related reviews inside each game
class GameSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'
