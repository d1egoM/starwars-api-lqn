from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from starwars.models import Planet, Character, Director, Producer, Movie
from schema import schema  
from datetime import date

class StarWarsGraphQLTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        # Set up initial data for tests: one planet, one character, one director, one producer, and one movie

        self.planet = Planet.objects.create(name="Tatooine", climate="arid", population=200000)

        self.character = Character.objects.create(
            name="Luke Skywalker",
            birth_year="19BBY",
            gender="male",
            species="Human",
            affiliation="Rebellion",
            homeworld=self.planet
        )

        self.director = Director.objects.create(
            name="George Lucas",
            birth_year="1944",
            gender="male",
            homeworld=self.planet,
            awards="Academy Award",
            is_active=True
        )

        self.producer = Producer.objects.create(
            name="Rick McCallum",
            birth_year="1950",
            gender="male",
            homeworld=self.planet,
            production_company="Lucasfilm",
            is_active=True
        )

        self.movie = Movie.objects.create(
            title="A New Hope",
            episode_id=4,
            opening_crawl="It is a period of civil war...",
            release_date=date(1977, 5, 25),
            director=self.director
        )
        self.movie.characters.add(self.character)
        self.movie.producers.add(self.producer)
        self.movie.planets.add(self.planet)

    def test_query_all_movies(self):
        """Test fetching all movies with related entities"""
        response = self.query(
            '''
            query {
                allMovies {
                    title
                    episodeId
                    releaseDate
                    director { name }
                    characters { name }
                    producers { name }
                    planets { name }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = response.json()
        self.assertEqual(content["data"]["allMovies"][0]["title"], "A New Hope")

    def test_filter_character_by_name(self):
        """Test filtering characters by name"""
        response = self.query(
            '''
            query {
                allCharacters(name: "Luke") {
                    name
                    species
                    affiliation
                    homeworld { name }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = response.json()
        self.assertEqual(content["data"]["allCharacters"][0]["name"], "Luke Skywalker")

    def test_create_planet_mutation(self):
        """Test creating a new planet"""
        response = self.query(
            '''
            mutation {
                createPlanet(name: "Naboo", climate: "temperate", population: 4500000000) {
                    planet {
                        name
                        climate
                        population
                    }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = response.json()
        self.assertEqual(content["data"]["createPlanet"]["planet"]["name"], "Naboo")

    def test_create_character_mutation(self):
        """Test creating a new character associated with an existing planet"""
        response = self.query(
            '''
            mutation {
                createCharacter(
                    name: "Leia Organa",
                    birthYear: "19BBY",
                    gender: "female",
                    species: "Human",
                    affiliation: "Rebellion",
                    homeworldId: "%s"
                ) {
                    character {
                        name
                        species
                        homeworld { name }
                    }
                }
            }
            ''' % self.planet.id
        )
        self.assertResponseNoErrors(response)
        content = response.json()
        self.assertEqual(content["data"]["createCharacter"]["character"]["name"], "Leia Organa")

    def test_create_movie_with_existing_data(self):
        """Test creating a movie using existing related objects (director, producer, character, planet)"""
        response = self.query(
            '''
            mutation {
                createMovie(
                    title: "The Empire Strikes Back",
                    episodeId: 5,
                    openingCrawl: "It is a dark time for the Rebellion...",
                    directorId: "%s",
                    producerIds: ["%s"],
                    characterIds: ["%s"],
                    planetIds: ["%s"],
                    releaseDate: "1980-05-21"
                ) {
                    movie {
                        title
                        director { name }
                        producers { name }
                        characters { name }
                        planets { name }
                    }
                }
            }
            ''' % (self.director.id, self.producer.id, self.character.id, self.planet.id)
        )
        self.assertResponseNoErrors(response)
        content = response.json()
        self.assertEqual(content["data"]["createMovie"]["movie"]["title"], "The Empire Strikes Back")