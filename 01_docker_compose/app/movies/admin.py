from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmWorkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres',)
    list_filter = ('type', 'creation_date', 'rating',)
    search_fields = ('title', 'description', 'id',)
    list_prefetch_related = ('persons', 'genres')

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Жанры фильма'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)
