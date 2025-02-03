from django.conf.urls.static import static
from django.urls import path, re_path

from . import views
from .views import *

app_name = 'bench'

urlpatterns = [
    # path('', views.news, name='home'),
    path('', views.main_page, name='main_page'),
    path('profile', views.profile, name='profile'),

    re_path(r'^profile/callback/$', views.callback_join, name='authds'),

    path('discord/callback/', views.callback_join, name='discord_callback'),
    # path('discord/login/', views.discord_login, name='discord_login'),
]