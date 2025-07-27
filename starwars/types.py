import graphene
from graphene_django import DjangoObjectType
from .models import Movie, Character, Director, Producer, Planet


# The `PlanetType` class is a DjangoObjectType representing a model for a Planet with all fields
# included.
class PlanetType(DjangoObjectType):
    class Meta:
        model = Planet
        fields = "__all__"


# The `CharacterType` class defines a GraphQL type for a character with a field representing their
# homeworld.
class CharacterType(DjangoObjectType):
    class Meta:
        model = Character
        fields = "__all__"

    homeworld = graphene.Field(PlanetType)

    def resolve_homeworld(self, info):
        return self.homeworld


# The `DirectorType` class is a DjangoObjectType representing a Director model with an additional
# field `homeworld` of type `PlanetType`.
class DirectorType(DjangoObjectType):
    class Meta:
        model = Director
        fields = "__all__"

    homeworld = graphene.Field(PlanetType)

    def resolve_homeworld(self, info):
        return self.homeworld


# The `ProducerType` class is a DjangoObjectType representing a Producer model with an additional
# field `homeworld` of type `PlanetType` that can be resolved to return the homeworld of the producer.
class ProducerType(DjangoObjectType):
    class Meta:
        model = Producer
        fields = "__all__"

    homeworld = graphene.Field(PlanetType)

    def resolve_homeworld(self, info):
        return self.homeworld


# The `MovieType` class defines a GraphQL type for movies with fields for director, producers,
# characters, and planets, along with resolver functions to fetch related data.
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        fields = "__all__"

    director = graphene.Field(DirectorType)
    producers = graphene.List(ProducerType)
    characters = graphene.List(CharacterType)
    planets = graphene.List(PlanetType)

    def resolve_director(self, info):
        return self.director

    def resolve_producers(self, info):
        return self.producers.all()

    def resolve_characters(self, info):
        return self.characters.all()

    def resolve_planets(self, info):
        return self.planets.all()
