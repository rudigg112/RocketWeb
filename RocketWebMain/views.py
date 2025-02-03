from django.contrib.auth import login
from django.contrib.sites import requests
from django.shortcuts import render, redirect

from RocketWeb.settings import DISCORD_CLIENT_ID, REDIRECT_URI_JOIN, DISCORD_CLIENT_SECRET, DISCORD_SERVER_ID

import requests

from RocketWebMain.db_client import DBClient
from RocketWebMain.models import DiscordUser


# Create your views here.


def main_page(request):
    if request.user.is_authenticated:
        return render(request, 'RocketWebMain/home_page.html')
    else:
        return redirect('/login')


def profile(request):
    if request.user.is_authenticated:
        db = DBClient()
        print('соединение', db)
        query_select_user_info = """
                SELECT CONCAT_WS(' ', u_info.surname, u_info.name, u_info.patronymic) AS full_name, ## 0
                u_info.date_birth,  ## 1
                u_info.country_location,  ## 2
                u_info.city,  ## 3
                u_info.country_of_tax,  ## 4
                u_info.telegram_nickname, ## 5
                u_info.phone_number, ## 6
                u_info.email, ## 7
                u_info.role, ## 8
                u_info.email_for_notion, ## 9
                u_info.email_for_alfa, ## 10
                u_info.email_for_omnidesk, ## 11
                u_info.legal_status, ## 12
                u_info.payment_receive, ## 13
                u_info.legal_status, ## 14
                u_info.payment_requisites, ## 15
                u_info.departament, ## 16
                u_info.rocket_coins, ## 17
                u_info.phone_number_reserve ## 18
                FROM user AS u INNER JOIN user_info AS u_info ON u_info.user_obj_id = u.id 
                WHERE u.user_id = %s
                """

        user_info = db.select_fetchone(query_select_user_info, (request.user.discord_id,))
        print('данные получены', user_info)
        db.exit_db()
        print('соединение закрыто', user_info[1].strftime('%d.%m.%Y'))

        data = {
            'user_info': {
                'full_name': user_info[0],
                'date_birth': user_info[1].strftime('%Y-%m-%d') if user_info[1] else "",
                'country_location': user_info[2].title() if user_info[2] else "",
                'city': user_info[3].title() if user_info[3] else "",
                'country_of_tax': user_info[4].title() if user_info[4] else "",
                'telegram_nickname': user_info[5],
                'phone_number': user_info[6],
                'email': user_info[7],
                'role': user_info[8].title() if user_info[8] else "",
                'email_for_notion': user_info[9],
                'email_for_alfa': user_info[10],
                'email_for_omnidesk': user_info[11],
                'legal_status': user_info[12].title() if user_info[16] else "",
                'payment_receive': user_info[13].title() if user_info[16] else "",
                'payment_requisites': user_info[15],
                'departament': user_info[16].title() if user_info[16] else "",
                'rocket_coins': user_info[17],
                'phone_number_reserve': user_info[18],
            }
        }

        return render(request, 'RocketWebMain/profile.html', data)
    return redirect('/login')


def login_page(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        print(request.POST)
        if 'ds_auth' in request.POST:
            request.session['create_url_profile'] = request.path
            discord_auth_url = f'https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri=' \
                               f'{REDIRECT_URI_JOIN}&response_type=code&scope=identify'
            return redirect(discord_auth_url)

    return render(request, 'RocketWebAuth/login.html')


def callback_join(request):
    code = request.GET.get('code')
    if not code:
        return redirect('/')

    # Получение токена
    token_url = 'https://discord.com/api/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI_JOIN,
        'scope': 'identify guilds',
    }
    response = requests.post(token_url, headers=headers, data=data)

    print('response', response)
    if response.status_code != 200:
        return redirect('/')

    access_token = response.json().get('access_token')

    # Получение данных пользователя
    user_info_url = 'https://discord.com/api/v10/users/@me'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(user_info_url, headers=headers)

    print('response2', response)
    if response.status_code != 200:
        return redirect('/')

    user_data = response.json()
    discord_id = user_data.get('id')
    username = user_data.get('username')
    avatar_hash = user_data.get('avatar')
    avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar_hash}.png"

    # Проверка, состоит ли пользователь в сервере
    guilds_url = 'https://discord.com/api/v10/users/@me/guilds'
    response = requests.get(guilds_url, headers=headers)
    is_in_server = False
    print('response3', response)
    if response.status_code == 200:
        guilds = response.json()
        is_in_server = any(guild['id'] == DISCORD_SERVER_ID for guild in guilds)

    # Создание или обновление пользователя
    user, created = DiscordUser.objects.get_or_create(discord_id=discord_id, defaults={
        'username': username,
        'avatar_url': avatar_url,
    })

    print('user, created', user, created)

    # Установка статуса, если пользователь на сервере
    if is_in_server:
        user.status = 'employee'  # Сотрудник
        user.save()

    # Вход пользователя
    login(request, user)

    redirect_url = request.session.get('create_url_profile', '/')
    print(redirect_url)
    return redirect('/')
