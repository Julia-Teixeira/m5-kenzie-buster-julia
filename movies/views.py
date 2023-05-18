from rest_framework.views import APIView, Response, Request
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from users.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request: Request):
        validate_data = MovieSerializer(data=request.data)
        validate_data.is_valid(raise_exception=True)

        validadated_data = validate_data.save(user=request.user)

        formated_data = MovieSerializer(instance=validadated_data)

        return Response(formated_data.data, 201)

    def get(self, request: Request):
        movies = Movie.objects.all()
        results_movies = self.paginate_queryset(movies, request)
        movies_serializer = MovieSerializer(instance=results_movies, many=True)

        return self.get_paginated_response(movies_serializer.data)


class MovieDetailsView(APIView):
    def get(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)
        movie_serializer = MovieSerializer(movie)
        return Response(movie_serializer.data)

    permission_classes = [IsAdminOrReadOnly]

    def delete(self, resquest: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        return Response(status=204)


class MovieOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id):
        movie_data = get_object_or_404(Movie, id=movie_id)

        movie_order = MovieOrderSerializer(data=request.data)
        movie_order.is_valid(raise_exception=True)

        validated_data = movie_order.save(user=request.user, movie=movie_data)

        formated_data = MovieOrderSerializer(instance=validated_data)
        return Response(formated_data.data, 201)
