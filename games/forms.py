from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game

        fields = ['title',
                  'genre',
                  'developer',
                  'mode_game',
                  'platform',
                  'system_requirements',
                  'release_date',
                  'raiting',
                  'price',
                  'image',
                  ]
