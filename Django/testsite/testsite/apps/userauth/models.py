from django.db import models


class User(models.Model):
    username = models.CharField('Username', max_length=50)
    password = models.CharField('Password', max_length=50)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserFriend(models.Model):
    whose_friend_key = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_username = models.CharField('FriendUsername', max_length=50)
    friend_password = models.CharField('FriendPassword', max_length=50)

    class Meta:
        verbose_name = 'Друг пользователя'
        verbose_name_plural = 'Друзья пользователей'
