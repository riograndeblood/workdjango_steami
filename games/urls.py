from rest_framework.routers import SimpleRouter
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views


# (
#     GameListView,
#     GameDetailView,
#     get_genre_games,
#     search_game,
#     # search_game_by_genre,
#     add_comment,
#     favorites,
#     favorite_game,
#     delete_from_favorites,
#
#     # JSON!!!
#     GameViewSet,
#     get_all_games,
#     game_detail,
#     GenreList,
#     GenreDetailView,
#     genre_detail,
#     get_all_genre,
#     UserList,
#     get_all_users,
#
#
# )

# router = routers.DefaultRouter()
# router.register('games', views.GameViewSet, basename='games')

# router.register('genres', views.GenreViewSet),
# router.register('users', views.UserViewSet)


urlpatterns = [
    path("get_games/", views.GameListView.as_view(), name="games"),
    path("detail_games/<int:pk>/", views.GameDetailView.as_view(), name="get_game"),
    path("get_genre_games/<str:title>/", views.get_genre_games, name="get_genre_games"),
    path("search_game/", views.search_game, name="search_game"),
    # path("search_game_by_genre/", search_game_by_genre, name="search_game_by_genre"),
    path("add_comment/<int:id>/", views.add_comment, name="add_comment"),
    path("delete_comment/<int:id>/", views.delete_comment, name='delete_comment'),
    path("favorite/<int:id>/", views.favorite_game, name="favorite_game"),
    path("favorites/", views.favorites, name="favorites"),
    path("delete_from_favorites/<int:id>/",views.delete_from_favorites,name="delete_from_favorites",),
    path("delete_game/<int:id>/", views.delete_game, name="delete_game"),
    path("add_game/", views.add_game, name="add_game"),
#   JSON!



    # path("get_all_games/", views.get_all_games),
    # path("get_game/<int:id>/", views.game_detail),

    path("api/games/", views.GameAPIList.as_view()),
    path("api/games/<int:pk>/", views.GameAPIUpdate.as_view()),
    path("api/games_delete/<int:pk>/", views.GameAPIDestroy.as_view()),
    path("api/genres/", views.GenreAPIList.as_view()),
    path("api/genres/<int:pk>/", views.GenreAPIDetail.as_view()),






]


# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT)
#     urlpatterns += router.urls
