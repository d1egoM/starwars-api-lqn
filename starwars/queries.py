import graphene
from .types import MovieType, CharacterType, PlanetType
from .models import Movie, Character, Planet

# The `Query` class defines GraphQL queries to retrieve all movies, a specific movie by ID, characters
# by name, and all planets.
class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int())
    all_characters = graphene.List(CharacterType, name=graphene.String())
    all_planets = graphene.List(PlanetType)

    def resolve_all_movies(self, info):
        return Movie.objects.all()

    def resolve_movie(self, info, id):
        return Movie.objects.filter(pk=id).first()

    def resolve_all_characters(self, info, name=None):
        if name:
            return Character.objects.filter(name__icontains=name)
        return Character.objects.all()

    def resolve_all_planets(self, info):
        return Planet.objects.all()
