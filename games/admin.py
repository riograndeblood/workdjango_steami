from django.contrib import admin

from .models import (Game,
                     Genre,
                     Developer,
                     Mode,
                     Platform,
                     System_requirements,
                     Comment,
                     Favorite,
                     )

class GameAdmin(admin.ModelAdmin):
    list_display_links = ('title','id')
    search_fields = ('title',)
    list_display = ('id',
                    'title',
                    'get_genre',
                    'get_developer',
                    'get_mode_game',
                    'get_platform',
                    'system_requirements',
                    'release_date',
                    'raiting',
                    'price',
                    'image',
                    'user')

    def get_genre(self,obj):
        genre = obj.genre.all()
        return "\n".join([str(g) for g in genre])
    def get_mode_game(self,obj):
        mode_game = obj.mode_game.all()
        return "\n".join([str(m) for m in mode_game])
    def get_platform(self,obj):
        platform = obj.platform.all()
        return "\n".join([str(p) for p in platform])
    def get_developer(self,obj):
        developer = obj.developer.all()
        return "\n".join([str(p) for p in developer])


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)

class ModeAdmin(admin.ModelAdmin):
    list_display = ('title',)

class PlatformAdmin(admin.ModelAdmin):
    list_display = ('title',)

class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('title',)



admin.site.register(Game, GameAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Mode, ModeAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(System_requirements)
admin.site.register(Comment)
admin.site.register(Favorite)
