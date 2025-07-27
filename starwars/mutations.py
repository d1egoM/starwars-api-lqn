import graphene
from .models import Character, Movie, Planet, Director, Producer
from .types import CharacterType, MovieType, PlanetType, DirectorType, ProducerType


# The above code defines GraphQL mutations for creating characters, directors, producers, planets, and
# movies in a Star Wars-themed application.
class CreateCharacter(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        birth_year = graphene.String(required=True)
        gender = graphene.String(required=True)
        species = graphene.String()
        affiliation = graphene.String()
        homeworld_id = graphene.ID()

    character = graphene.Field(CharacterType)

    def mutate(self, info, name, birth_year, gender, species=None, affiliation=None, homeworld_id=None):
        character = Character.objects.create(
            name=name,
            birth_year=birth_year,
            gender=gender,
            species=species,
            affiliation=affiliation,
            homeworld_id=homeworld_id
        )
        return CreateCharacter(character=character)


class CreateDirector(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        birth_year = graphene.String(required=True)
        gender = graphene.String(required=True)
        homeworld_id = graphene.ID()
        awards = graphene.String()
        is_active = graphene.Boolean()

    director = graphene.Field(DirectorType)

    def mutate(self, info, name, birth_year, gender, homeworld_id=None, awards=None, is_active=True):
        director = Director.objects.create(
            name=name,
            birth_year=birth_year,
            gender=gender,
            homeworld_id=homeworld_id,
            awards=awards or "",
            is_active=is_active
        )
        return CreateDirector(director=director)


class CreateProducer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        birth_year = graphene.String(required=True)
        gender = graphene.String(required=True)
        homeworld_id = graphene.ID()
        production_company = graphene.String()
        is_active = graphene.Boolean()

    producer = graphene.Field(ProducerType)

    def mutate(self, info, name, birth_year, gender, homeworld_id=None, production_company=None, is_active=True):
        producer = Producer.objects.create(
            name=name,
            birth_year=birth_year,
            gender=gender,
            homeworld_id=homeworld_id,
            production_company=production_company or "",
            is_active=is_active
        )
        return CreateProducer(producer=producer)


class CreatePlanet(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        climate = graphene.String(required=True)
        population = graphene.BigInt()

    planet = graphene.Field(PlanetType)

    def mutate(self, info, name, climate, population=None):
        planet = Planet.objects.create(
            name=name,
            climate=climate,
            population=population
        )
        return CreatePlanet(planet=planet)


class CreateMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        episode_id = graphene.Int(required=True)
        opening_crawl = graphene.String()
        director_id = graphene.ID(required=True)
        producer_ids = graphene.List(graphene.ID)
        character_ids = graphene.List(graphene.ID)
        planet_ids = graphene.List(graphene.ID)
        release_date = graphene.types.datetime.Date(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, title, episode_id, director_id, release_date,
               opening_crawl=None, producer_ids=None, character_ids=None, planet_ids=None):
        movie = Movie.objects.create(
            title=title,
            episode_id=episode_id,
            opening_crawl=opening_crawl or "",
            director_id=director_id,
            release_date=release_date
        )
        if producer_ids:
            movie.producers.set(producer_ids)
        if character_ids:
            movie.characters.set(character_ids)
        if planet_ids:
            movie.planets.set(planet_ids)
        return CreateMovie(movie=movie)


class Mutation(graphene.ObjectType):
    create_character = CreateCharacter.Field()
    create_director = CreateDirector.Field()
    create_producer = CreateProducer.Field()
    create_planet = CreatePlanet.Field()
    create_movie = CreateMovie.Field()