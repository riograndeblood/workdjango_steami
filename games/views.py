from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .models import (
    Game,
    Genre,
    Developer,
    Mode,
    Platform,
    Favorite,
    System_requirements,
    Comment,
    User,
)
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics, viewsets
from django.http import JsonResponse

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (GameSerializer,

                          UserSerializer, GenreGameSerializer, GenreSerializer, )
from .forms import GameForm
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny,
                                        IsAuthenticatedOrReadOnly,
                                        IsAdminUser)


#       Возврат в виде Json в панели Django REST framework

#          Просмотр всех игр и создание-->(только для авторизованного)
class GameAPIList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

#     Даёт права изменять только свою запись по id если ты авторизован
class GameAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
        # authentication_classes = (TokenAuthentication, )


#         Удаление игры по id (только для админа)
class GameAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (IsAdminOrReadOnly, )

#          Просмотр всех жанров и игр которые есть у одного жанра
#          По аналогии можно сделать просмотр любых данных из бд
class GenreAPIList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

#           Просмотр одного жанра по id и список его игр
class GenreAPIDetail(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


#
# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



# #       Возврат в виде Json
# def get_all_games(request):
#         games = Game.objects.all()
#         serializer = GameSerializer(games, many=True)
#         return JsonResponse(data=serializer.data, safe=False)
# def game_detail(request, id):
#         try:
#             game = Game.objects.get(id=id)
#         except Game.DoesNotExist:
#             return JsonResponse(data={'id': 'Game not found'})
#         serializer = GameSerializer(game)
#         return JsonResponse(data=serializer.data)





class GameListView(ListView):
    model = Game
    context_object_name = "all_games"
    queryset = Game.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = Genre.objects.all()
        context["genre"] = genre
        return context

class GameDetailView(DetailView):
    model = Game
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        show_favorite_button = True
        if self.request.user.is_authenticated:
            if Favorite.objects.filter(game=game, user=self.request.user):
                show_favorite_button = False
            context["show_favorite_button"] = show_favorite_button
        return context

def get_genre_games(request, title):
    try:
        genre = Genre.objects.get(title=title)
    except Genre.DoesNotExist:
        return HttpResponse(f"<f1>{title} not exist<1/>")
    genre_games = genre.games.all()
    return render(
        request,
        "genre_detail.html",
        context={"genre_games": genre_games, "genre": genre
        },
    )


def search_game(request):
    title = request.GET["title"]
    games = Game.objects.all()
    if title != "":
        games = games.filter(title__contains=title)
    return render(
        request,
        "search_game.html",
        context={
            "games": games,
        },
    )

def add_game(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = GameForm(request.POST, request.FILES)
            if form.is_valid():
                game = form.save(commit=False)
                game.user = request.user
                game.save()
                return redirect("games")
        else:
            form = GameForm
        data = {
            'form':form
        }
        return render(request, 'add_game.html', data)
    else:
        return redirect("login")



def delete_game(request, id):
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return HttpResponse(f"<h1>Книга с id: {id} удалена!</h1>")
    if request.user.username != game.user.username:
        return HttpResponse(f"<h1>У вас нет прав!!</h1>")
    else:
        game.delete()
        return redirect("games")

def add_comment(request, id):
    if request.user.is_authenticated:
        try:
            game = Game.objects.get(id=id)
        except Game.DoesNotExist:
            return HttpResponse(f"<h1>Games with id {id} do not exist</h1>")
        try:
            Comment.objects.create(
                content=request.POST["comment"],
                user=request.user,
                game=game
            )
        except MultiValueDictKeyError:
            return HttpResponse(f"<h1>404</h1>")
        return redirect('get_game', pk=game.id)
    else:
        return HttpResponse(f"<h1>Вы не авторизованы</h1>")


def delete_comment(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return HttpResponse(f"<h1>Коментарий с id: {id} удалён!</h1>")
    if request.user.username != comment.user.username:
        return HttpResponse(f"<h1>У вас нет прав!!</h1>")
    else:
        comment.delete()
        return redirect("get_game", pk=comment.game.id)

def favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request,
                      "favorite_game.html",
                      context={"favorites": favorites})
    else:
        return HttpResponse("<h1>404</h1>")

def favorite_game(request, id):
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return HttpResponse(f"<h1>404</h1>")
    if not request.user.is_authenticated:
        return HttpResponse(f"<h1>404</h1>")
    Favorite.objects.create(game=game,
                            user=request.user,

                            )
    return redirect("get_game", pk=game.id)


def delete_from_favorites(request, id):
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return HttpResponse(f"<h1>404</h1>")
    if request.user.is_authenticated:
        favorite = Favorite.objects.get(user=request.user, game=game)
        favorite.delete()
        return redirect("favorites")
    return HttpResponse(f"<h1>404</h1>")
