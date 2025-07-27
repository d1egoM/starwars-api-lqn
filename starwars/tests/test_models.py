from django.test import TestCase
from starwars.models import Planet, Character, Director, Producer, Movie
from datetime import date

# Test for the Planet model
class PlanetModelTest(TestCase):
    def test_create_planet(self):
        # Create a planet and check its fields
        planet = Planet.objects.create(name="Dagobah", climate="swampy", population=0)
        self.assertEqual(planet.name, "Dagobah")
        self.assertEqual(planet.climate, "swampy")
        self.assertEqual(planet.population, 0)

# Test for the Character model
class CharacterModelTest(TestCase):
    def setUp(self):
        # Create a planet as a required foreign key
        self.planet = Planet.objects.create(name="Alderaan", climate="temperate", population=2000000000)

    def test_create_character(self):
        # Create a character and validate its relationship with the planet
        character = Character.objects.create(
            name="Obi-Wan Kenobi",
            birth_year="57BBY",
            gender="male",
            species="Human",
            affiliation="Jedi Order",
            homeworld=self.planet
        )
        self.assertEqual(character.name, "Obi-Wan Kenobi")
        self.assertEqual(character.homeworld.name, "Alderaan")

# Test for the Director model
class DirectorModelTest(TestCase):
    def setUp(self):
        # Create a planet for the director
        self.planet = Planet.objects.create(name="Coruscant", climate="urban", population=10000000000)

    def test_create_director(self):
        # Create a director and validate its fields
        director = Director.objects.create(
            name="Rian Johnson",
            birth_year="1973",
            gender="male",
            homeworld=self.planet,
            awards="Oscar",
            is_active=True
        )
        self.assertEqual(director.name, "Rian Johnson")
        self.assertTrue(director.is_active)

# Test for the Producer model
class ProducerModelTest(TestCase):
    def setUp(self):
        # Create a planet for the producer
        self.planet = Planet.objects.create(name="Mustafar", climate="lava", population=1000)

    def test_create_producer(self):
        # Create a producer and validate its information
        producer = Producer.objects.create(
            name="Kathleen Kennedy",
            birth_year="1953",
            gender="female",
            homeworld=self.planet,
            production_company="Lucasfilm",
            is_active=False
        )
        self.assertEqual(producer.name, "Kathleen Kennedy")
        self.assertEqual(producer.production_company, "Lucasfilm")
        self.assertFalse(producer.is_active)

# Test for the Movie model and many-to-many relationships
class MovieModelTest(TestCase):
    def setUp(self):
        # Create shared data: planet, character, director, producer
        self.planet = Planet.objects.create(name="Endor", climate="forest", population=30000)
        self.character = Character.objects.create(
            name="Han Solo",
            birth_year="29BBY",
            gender="male",
            species="Human",
            affiliation="Rebellion",
            homeworld=self.planet
        )
        self.director = Director.objects.create(
            name="Irvin Kershner",
            birth_year="1923",
            gender="male",
            homeworld=self.planet,
            awards="Emmy",
            is_active=True
        )
        self.producer = Producer.objects.create(
            name="Gary Kurtz",
            birth_year="1940",
            gender="male",
            homeworld=self.planet,
            production_company="Lucasfilm",
            is_active=True
        )

    def test_create_movie_with_relations(self):
        # Create a movie and add many-to-many relations
        movie = Movie.objects.create(
            title="Return of the Jedi",
            episode_id=6,
            opening_crawl="Luke Skywalker has returned to his home planet...",
            release_date=date(1983, 5, 25),
            director=self.director
        )
        movie.characters.add(self.character)
        movie.producers.add(self.producer)
        movie.planets.add(self.planet)

        # Validate direct fields and relationships
        self.assertEqual(movie.title, "Return of the Jedi")
        self.assertIn(self.character, movie.characters.all())
        self.assertIn(self.producer, movie.producers.all())
        self.assertIn(self.planet, movie.planets.all())


class ModelIntegrityTests(TestCase):
    def setUp(self):
        # Create base planet
        self.planet = Planet.objects.create(name="Tatooine", climate="arid", population=200000)

        # Create related director
        self.director = Director.objects.create(
            name="George Lucas",
            birth_year="1944",
            gender="male",
            homeworld=self.planet,
            awards="Academy Award",
            is_active=True
        )

        # Create related producer
        self.producer = Producer.objects.create(
            name="Rick McCallum",
            birth_year="1950",
            gender="male",
            homeworld=self.planet,
            production_company="Lucasfilm",
            is_active=True
        )

        # Create related character
        self.character = Character.objects.create(
            name="Luke Skywalker",
            birth_year="19BBY",
            gender="male",
            species="Human",
            affiliation="Rebellion",
            homeworld=self.planet
        )

        # Create movie and associate all related entities
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

    def test_movie_relationships_integrity(self):
        """Ensure the movie is properly linked to characters, producers, planets, and director."""
        self.assertIn(self.character, self.movie.characters.all())
        self.assertIn(self.producer, self.movie.producers.all())
        self.assertIn(self.planet, self.movie.planets.all())
        self.assertEqual(self.movie.director, self.director)

    def test_cascade_delete_planet_removes_character(self):
        """Check that deleting a planet sets character homeworld to null if SET_NULL is used."""
        self.planet.delete()
        self.assertIsNone(Character.objects.get(name="Luke Skywalker").homeworld)

    def test_prevent_duplicate_director_name(self):
        """Attempt to create a director with the same name should raise an error if 'name' is unique."""
        with self.assertRaises(Exception):
            Director.objects.create(
                name="George Lucas",  # Duplicate name
                birth_year="1950",
                gender="male",
                homeworld=self.planet,
                awards="None",
                is_active=False
            )

    def test_required_field_on_character(self):
        """Character creation without a name should fail due to non-null constraint."""
        with self.assertRaises(Exception):
            Character.objects.create(
                name=None,
                birth_year="20BBY",
                gender="male",
                species="Human",
                affiliation="Empire",
                homeworld=self.planet
            )

    def test_create_movie_with_multiple_relations(self):
        """Create a movie linked to multiple characters and producers."""
        new_character = Character.objects.create(
            name="Han Solo",
            birth_year="29BBY",
            gender="male",
            species="Human",
            affiliation="Rebellion",
            homeworld=self.planet
        )
        self.movie.characters.add(new_character)
        self.assertIn(new_character, self.movie.characters.all())
