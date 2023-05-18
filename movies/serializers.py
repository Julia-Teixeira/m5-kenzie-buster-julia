from rest_framework import serializers
from .models import RatingChoices, Movie, MovieOrder
from users.serializers import UserSerializer
from users.models import User


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False, default="null")
    rating = serializers.ChoiceField(
        choices=RatingChoices.choices,
        default=RatingChoices.G,
        required=False,
    )
    synopsis = serializers.CharField(default=None, required=False, max_length=255)
    added_by = serializers.CharField(source="user.email", read_only=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True, source="movie.title")
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.CharField(source="user.email", read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)
