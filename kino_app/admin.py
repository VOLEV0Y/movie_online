from django.contrib import admin
from .models import Genre, Film, Review

class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'director', 'display_genres', 'created_at']
    list_filter = ['genres', 'year']
    search_fields = ['title', 'director', 'description']
    filter_horizontal = ['genres']
    
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Жанры'

admin.site.register(Genre)
admin.site.register(Film, FilmAdmin)
admin.site.register(Review)