from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

class GameList(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameDetail(APIView):
    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return None

    def get(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        game.delete()
        return Response({'message': 'Game deleted'}, status=status.HTTP_200_OK)

class ReviewList(APIView):
    def get(self, request, pk):
        game = Game.objects.filter(pk=pk).first()
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        reviews = Review.objects.filter(game=game)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        game = Game.objects.filter(pk=pk).first()
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(game=game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameRecommendation(APIView):
    def get(self, request):
        genre = request.query_params.get('genre', None)
        platform = request.query_params.get('platform', None)
        age_rating = request.query_params.get('age_rating', None)
        min_score = request.query_params.get('min_score', None)

        games = Game.objects.all()

        if genre:
            games = games.filter(genre__icontains=genre)
        if platform:
            games = games.filter(platform__icontains=platform)
        if age_rating:
            games = games.filter(age_rating__icontains=age_rating)
        if min_score:
            try:
                games = games.filter(critic_score__gte=float(min_score))
            except ValueError:
                return Response(
                    {'error': 'min_score must be a number'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        games = games.filter(
            critic_score__isnull=False
        ).order_by('-critic_score')[:10]

        if not games.exists():
            return Response(
                {'message': 'No games found matching your preferences'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GameSerializer(games, many=True)
        return Response({
            'message': f'Top {games.count()} recommended games for you',
            'filters_applied': {
                'genre': genre,
                'platform': platform,
                'age_rating': age_rating,
                'min_score': min_score
            },
            'recommendations': serializer.data
        }, status=status.HTTP_200_OK)

