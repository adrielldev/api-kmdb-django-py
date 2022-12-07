from rest_framework import serializers
from genre.serializers import GenreSerializer
from .models import Movie
from genre.models import Genre

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length = 127)
    duration = serializers.CharField(max_length = 10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True)

    def create(self,validated_data:dict):
        genre_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        for genre in genre_data:
            g = Genre.objects.get_or_create(name=GenreSerializer(genre).data['name'])[0]
            movie.genres.add(g)

        return movie

    def update(self,instance:Movie,validated_data:dict):
        genre_data = validated_data.pop('genres')

        instance.title = validated_data.get('title',instance.title)
        instance.duration = validated_data.get('duration',instance.duration)
        instance.premiere = validated_data.get('premiere',instance.premiere)
        instance.classification = validated_data.get('classification',instance.classification)
        instance.synopsis = validated_data.get('synopsis',instance.synopsis)
        if validated_data.get('genres'):
            instance.genres.set([])
        for genre in genre_data:
            g = Genre.objects.get_or_create(name=GenreSerializer(genre).data['name'])[0]
            instance.genres.add(g)
        
        instance.save()

        return instance


        return 
