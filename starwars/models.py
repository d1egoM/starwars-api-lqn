from django.db import models

# The `Planet` class defines a model with fields for name, climate, and population in a Django
# application.
class Planet(models.Model):
    name = models.CharField(max_length=100)
    climate = models.CharField(max_length=100)
    population = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


# This Python class defines a model for a character with attributes such as name, birth year, gender,
# homeworld, species, affiliation, and actor.
class Character(models.Model):
    name = models.CharField(max_length=100, unique=True)
    birth_year = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    homeworld = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True)
    species = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100)
    actor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


# The `Director` class defines a model with fields for name, birth year, gender, homeworld, awards,
# and active status.
class Director(models.Model):
    name = models.CharField(max_length=100, unique=True)
    birth_year = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    homeworld = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True)
    awards = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# The `Producer` class defines a model with fields for name, birth year, gender, homeworld, production
# company, and active status.
class Producer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    birth_year = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    homeworld = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True)
    production_company = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# The `Movie` class defines a model with fields for movie title, episode ID, opening crawl, release
# date, director, producers, characters, and planets in a Star Wars movie database.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField(blank=True)
    release_date = models.DateField()
    
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    producers = models.ManyToManyField(Producer, related_name="produced_movies", blank=True)
    characters = models.ManyToManyField(Character, related_name="movies", blank=True)
    planets = models.ManyToManyField(Planet, related_name="movies", blank=True)

    def __str__(self):
        return f"Episode {self.episode_id}: {self.title}"
