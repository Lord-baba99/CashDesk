from django.contrib.auth.decorators import login_required
from django.urls import path
from accounts.views import *

urlpatterns = [
    path("signup/", signup, name='signup'),
    path("logout/", logout_user, name='logout'),
    path("login/", login_user, name='login'),
    path("profile/", login_required(show_profile), name='profile'),
    path("update-profile/", login_required(update_profile), name='update-profile'),
]
