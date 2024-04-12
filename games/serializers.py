from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Game, Genre
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User





class GameSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    developer = serializers.SerializerMethodField()
    mode_game = serializers.SerializerMethodField()
    platform = serializers.SerializerMethodField()
    system_requirements = serializers.SerializerMethodField()
    # user = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Game
        fields = ['id',
                  'title',
                  'genre',
                  'developer',
                  'mode_game',
                  'platform',
                  'system_requirements',
                  'release_date',
                  'raiting',
                  'price',
                  'image',
                  'user']




    def get_genre(self, game):
        genres = []
        for g in game.genre.all():
            genres.append(g.title)
        return genres

    def get_developer(self, game):
        developers = []
        for d in game.developer.all():
            developers.append(d.title)
        return developers

    def get_mode_game(self, game):
        modes = []
        for m in game.mode_game.all():
            modes.append(m.title)
        return modes

    def get_platform(self, game):
        platforms = []
        for p in game.platform.all():
            platforms.append(p.title)
        return platforms

    def get_system_requirements(self, game):
        if game.system_requirements is not None:
            return game.system_requirements.link
        return None

    def get_user(self, obj):
        try:
            return obj.user.username
        except AttributeError:
            return None



class GenreGameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title']
class GenreSerializer(ModelSerializer):
    games = GenreGameSerializer(many=True)
    class Meta:
        model = Genre
        fields = ['id', 'title', 'games']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email']
