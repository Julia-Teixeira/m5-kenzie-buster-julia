from django.db import models
from users.models import User


class RatingChoices(models.TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127, null=False)
    duration = models.CharField(max_length=10, default=None, null=True)
    rating = models.CharField(
        max_length=20, choices=RatingChoices.choices, default=RatingChoices.G
    )
    synopsis = models.TextField(default=None, null=True)
    user = models.ForeignKey(User, related_name="movies", on_delete=models.RESTRICT)
    users = models.ManyToManyField(
        User, through="MovieOrder", related_name="movie_order"
    )

    def __str__(self) -> str:
        return f"title: {self.title}, added_by: {self.user.email}"


class MovieOrder(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    def __str__(self) -> str:
        return f"<user: {self.user.email} | movie: {self.movie.title} | price: {self.price}"
