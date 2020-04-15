from django.shortcuts import render
from .models import User, UserFriend


def index(request):
    list_of_users = User.objects.all()
    return render(request, 'userauth/friend_list.html', {'list_of_users': list_of_users})
