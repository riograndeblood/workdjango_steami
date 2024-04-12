from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=50)

    genre = models.ManyToManyField(
        "Genre",
        related_name="games",
        blank=True
    )
    developer = models.ManyToManyField(
        "Developer",
        related_name="games",
        blank=True
    )
    mode_game = models.ManyToManyField(
        "Mode",
        related_name="games",
        blank=True
    )
    platform = models.ManyToManyField(
        "Platform",
        related_name="games",
        blank=True
    )
    system_requirements = models.OneToOneField(
        'System_requirements',
        on_delete=models.DO_NOTHING,
        default=None,
        null=True,
        blank=True
    )
    release_date = models.DateField(blank=True,null=True)
    raiting = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='media/', default="default.jpg")
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'




class Genre(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Developer(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Mode(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Platform(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class System_requirements(models.Model):
    link = models.URLField(max_length=100)
    def __str__(self):
        return self.link

    class Meta:
        verbose_name = "Requirement"
        verbose_name_plural = "Requirements"


class Comment(models.Model):
    content = models.TextField(max_length=300)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='comments')

    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment : {self.content}, {self.user.username}"
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='favorites')
    game = models.ForeignKey(Game, on_delete=models.CASCADE,related_name='favorites')
    date_created = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.game.title}'
    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"



