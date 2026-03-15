from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


class GameList(APIView):
    @swagger_auto_schema(
        operation_summary="List all games",
        operation_description="""
        Returns a paginated list of all video games in the database.
        You can filter results using the following query parameters:
        - **genre**: Filter by genre (e.g. Action, Sports, Role-Playing)
        - **platform**: Filter by platform (e.g. PS4, PC, Wii)
        - **age_rating**: Filter by age rating (e.g. E, T, M)
        - **developer**: Filter by developer name
        - **year**: Filter by release year
        - **min_score**: Minimum critic score (0-100)
        - **max_score**: Maximum critic score (0-100)
        - **search**: Search games by title keyword
        - **ordering**: Sort by critic_score, -critic_score, release_year, -release_year, title, -title
        - **page**: Page number (20 results per page)
        """,
        manual_parameters=[
            openapi.Parameter('genre', openapi.IN_QUERY, description="Filter by genre e.g. Action", type=openapi.TYPE_STRING),
            openapi.Parameter('platform', openapi.IN_QUERY, description="Filter by platform e.g. PS4", type=openapi.TYPE_STRING),
            openapi.Parameter('age_rating', openapi.IN_QUERY, description="Filter by age rating e.g. E, T, M", type=openapi.TYPE_STRING),
            openapi.Parameter('developer', openapi.IN_QUERY, description="Filter by developer name", type=openapi.TYPE_STRING),
            openapi.Parameter('year', openapi.IN_QUERY, description="Filter by release year e.g. 2006", type=openapi.TYPE_INTEGER),
            openapi.Parameter('min_score', openapi.IN_QUERY, description="Minimum critic score e.g. 80", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_score', openapi.IN_QUERY, description="Maximum critic score e.g. 98", type=openapi.TYPE_NUMBER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search games by title keyword e.g. mario", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Sort results: critic_score, -critic_score, release_year, -release_year, title, -title", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number (20 results per page)", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(description="List of games returned successfully"),
            400: openapi.Response(description="Invalid filter parameters"),
        }
    )
    def get(self, request):
        games = Game.objects.all()
        genre = request.query_params.get('genre', None)
        platform = request.query_params.get('platform', None)
        age_rating = request.query_params.get('age_rating', None)
        developer = request.query_params.get('developer', None)
        year = request.query_params.get('year', None)
        min_score = request.query_params.get('min_score', None)
        max_score = request.query_params.get('max_score', None)
        search = request.query_params.get('search', None)
        ordering = request.query_params.get('ordering', None)
        if genre:
            games = games.filter(genre__icontains=genre)
        if platform:
            games = games.filter(platform__icontains=platform)
        if age_rating:
            games = games.filter(age_rating__icontains=age_rating)
        if developer:
            games = games.filter(developer__icontains=developer)
        if year:
            games = games.filter(release_year=year)
        if min_score:
            try:
                games = games.filter(critic_score__gte=float(min_score))
            except ValueError:
                return Response({'error': 'min_score must be a number'}, status=status.HTTP_400_BAD_REQUEST)
        if max_score:
            try:
                games = games.filter(critic_score__lte=float(max_score))
            except ValueError:
                return Response({'error': 'max_score must be a number'}, status=status.HTTP_400_BAD_REQUEST)
        if search:
            games = games.filter(title__icontains=search)
        valid_ordering = ['critic_score', '-critic_score', 'release_year', '-release_year', 'title', '-title']
        if ordering and ordering in valid_ordering:
            games = games.order_by(ordering)
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(games, request)
        serializer = GameSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new game",
        operation_description="Add a new video game to the database. All fields except developer, critic_score and age_rating are required.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'genre', 'platform'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the game e.g. The Last of Us"),
                'genre': openapi.Schema(type=openapi.TYPE_STRING, description="Genre e.g. Action, Sports, Role-Playing"),
                'platform': openapi.Schema(type=openapi.TYPE_STRING, description="Platform e.g. PS4, PC, Wii"),
                'release_year': openapi.Schema(type=openapi.TYPE_INTEGER, description="Year of release e.g. 2013"),
                'developer': openapi.Schema(type=openapi.TYPE_STRING, description="Developer studio e.g. Naughty Dog"),
                'critic_score': openapi.Schema(type=openapi.TYPE_NUMBER, description="Critic score out of 100 e.g. 95.0"),
                'age_rating': openapi.Schema(type=openapi.TYPE_STRING, description="Age rating e.g. E, T, M"),
            },
            example={
                "title": "The Last of Us",
                "genre": "Action",
                "platform": "PS3",
                "release_year": 2013,
                "developer": "Naughty Dog",
                "critic_score": 95.0,
                "age_rating": "M"
            }
        ),
        responses={
            201: openapi.Response(description="Game created successfully"),
            400: openapi.Response(description="Invalid data provided"),
        }
    )
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

    @swagger_auto_schema(
        operation_summary="Get a game by ID",
        operation_description="Retrieve full details of a single video game including all its reviews.",
        responses={
            200: openapi.Response(description="Game details returned successfully"),
            404: openapi.Response(description="Game not found"),
        }
    )
    def get(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a game",
        operation_description="Update all fields of an existing game by its ID.",
        request_body=GameSerializer,
        responses={
            200: openapi.Response(description="Game updated successfully"),
            400: openapi.Response(description="Invalid data provided"),
            404: openapi.Response(description="Game not found"),
        }
    )
    def put(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a game",
        operation_description="Permanently delete a game and all its associated reviews from the database.",
        responses={
            200: openapi.Response(description="Game deleted successfully"),
            404: openapi.Response(description="Game not found"),
        }
    )
    def delete(self, request, pk):
        game = self.get_object(pk)
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        game.delete()
        return Response({'message': 'Game deleted'}, status=status.HTTP_200_OK)


class ReviewList(APIView):
    @swagger_auto_schema(
        operation_summary="Get all reviews for a game",
        operation_description="Returns all user reviews for a specific game identified by its ID.",
        responses={
            200: openapi.Response(description="Reviews returned successfully"),
            404: openapi.Response(description="Game not found"),
        }
    )
    def get(self, request, pk):
        game = Game.objects.filter(pk=pk).first()
        if game is None:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        reviews = Review.objects.filter(game=game)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Add a review to a game",
        operation_description="Submit a new user review for a specific game. Rating must be between 1 and 10.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['reviewer_name', 'rating', 'comment'],
            properties={
                'reviewer_name': openapi.Schema(type=openapi.TYPE_STRING, description="Your name e.g. Zayed"),
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description="Rating from 1 to 10"),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description="Your review comment"),
            },
            example={
                "reviewer_name": "Zayed",
                "rating": 9,
                "comment": "One of the best games I have ever played!"
            }
        ),
        responses={
            201: openapi.Response(description="Review added successfully"),
            400: openapi.Response(description="Invalid data provided"),
            404: openapi.Response(description="Game not found"),
        }
    )
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
    @swagger_auto_schema(
        operation_summary="Get personalised game recommendations",
        operation_description="""
        Returns the top 10 highest rated games matching your preferences.
        All parameters are optional — combine them for more specific recommendations.
        - **genre**: Preferred genre (e.g. Action, Role-Playing, Sports)
        - **platform**: Preferred platform (e.g. PS4, PC, Wii)
        - **age_rating**: Age rating preference (e.g. E, T, M)
        - **min_score**: Minimum acceptable critic score (e.g. 80)

        Results are ordered by critic score from highest to lowest.
        Use GET /api/metadata/ to see all available genres and platforms.
        """,
        manual_parameters=[
            openapi.Parameter('genre', openapi.IN_QUERY, description="Preferred genre e.g. Action", type=openapi.TYPE_STRING),
            openapi.Parameter('platform', openapi.IN_QUERY, description="Preferred platform e.g. PS4", type=openapi.TYPE_STRING),
            openapi.Parameter('age_rating', openapi.IN_QUERY, description="Age rating e.g. E, T, M", type=openapi.TYPE_STRING),
            openapi.Parameter('min_score', openapi.IN_QUERY, description="Minimum critic score e.g. 80", type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: openapi.Response(description="Top 10 recommended games returned"),
            400: openapi.Response(description="Invalid parameter value"),
            404: openapi.Response(description="No games found matching preferences"),
        }
    )
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
                return Response({'error': 'min_score must be a number'}, status=status.HTTP_400_BAD_REQUEST)
        games = games.filter(critic_score__isnull=False).order_by('-critic_score')[:10]
        if not games.exists():
            return Response({'message': 'No games found matching your preferences'}, status=status.HTTP_404_NOT_FOUND)
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


class GameMetadata(APIView):
    @swagger_auto_schema(
        operation_summary="Get available filter values",
        operation_description="Returns all unique genres, platforms and age ratings available in the database. Use this endpoint to discover valid filter values before querying /api/games/ or /api/recommend/.",
        responses={
            200: openapi.Response(description="Available filter values returned successfully"),
        }
    )
    def get(self, request):
        genres = Game.objects.exclude(genre__isnull=True).values_list('genre', flat=True).distinct().order_by('genre')
        platforms = Game.objects.exclude(platform__isnull=True).values_list('platform', flat=True).distinct().order_by('platform')
        age_ratings = Game.objects.exclude(age_rating__isnull=True).values_list('age_rating', flat=True).distinct().order_by('age_rating')
        return Response({
            'message': 'Available filters for the Video Games API',
            'genres': list(genres),
            'platforms': list(platforms),
            'age_ratings': list(age_ratings),
        }, status=status.HTTP_200_OK)


class GameStats(APIView):
    @swagger_auto_schema(
        operation_summary="Get database statistics",
        operation_description="Returns overall statistics about the video games database including total games, average critic score, highest rated game, most common genre and platform, and a full breakdown of games per genre.",
        responses={
            200: openapi.Response(description="Statistics returned successfully"),
        }
    )
    def get(self, request):
        from django.db.models import Avg, Max, Min, Count
        total_games = Game.objects.count()
        total_reviews = Review.objects.count()
        avg_score = Game.objects.filter(critic_score__isnull=False).aggregate(Avg('critic_score'))['critic_score__avg']
        highest_rated = Game.objects.filter(critic_score__isnull=False).order_by('-critic_score').first()
        most_common_genre = Game.objects.values('genre').annotate(count=Count('genre')).order_by('-count').first()
        most_common_platform = Game.objects.values('platform').annotate(count=Count('platform')).order_by('-count').first()
        games_per_genre = Game.objects.values('genre').annotate(count=Count('genre')).order_by('-count')
        return Response({
            'total_games': total_games,
            'total_reviews': total_reviews,
            'average_critic_score': round(avg_score, 2) if avg_score else None,
            'highest_rated_game': {
                'title': highest_rated.title,
                'critic_score': highest_rated.critic_score,
                'platform': highest_rated.platform
            } if highest_rated else None,
            'most_common_genre': most_common_genre,
            'most_common_platform': most_common_platform,
            'games_per_genre': list(games_per_genre)
        }, status=status.HTTP_200_OK)
