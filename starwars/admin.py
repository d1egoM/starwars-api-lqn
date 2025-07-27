from django.contrib import admin
from .models import Character, Director, Producer, Planet, Movie

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'gender', 'birth_year', 'homeworld')
    search_fields = ('name', 'species', 'actor', 'affiliation')
    list_filter = ('gender', 'species', 'homeworld')
    ordering = ('name',)

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year', 'gender', 'homeworld', 'is_active')
    search_fields = ('name',)
    list_filter = ('gender', 'is_active', 'homeworld')
    ordering = ('name',)

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year', 'gender', 'homeworld', 'production_company', 'is_active')
    search_fields = ('name', 'production_company')
    list_filter = ('gender', 'is_active', 'homeworld')
    ordering = ('name',)

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'climate', 'population')
    search_fields = ('name', 'climate')
    list_filter = ('climate',)
    ordering = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'episode_id', 'release_date', 'director')
    search_fields = ('title', 'opening_crawl')
    list_filter = ('release_date', 'director', 'producers', 'planets')
    ordering = ('episode_id',)
    filter_horizontal = ('producers', 'characters', 'planets')
