import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from RocketWebMain.db_client import DBClient


@csrf_exempt
def save_profile_field(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field = data.get('field')
            value = data.get('value')
            user_id = request.user.discord_id  # Предполагается, что у пользователя есть discord_id

            if not field or not value:
                return JsonResponse({'success': False, 'error': 'Поле или значение не указаны'})

            db = DBClient()

            if field == 'full_name':
                # Логика для обработки full_name
                full_name = value.strip()
                name_parts = full_name.split(' ')

                if len(name_parts) == 1:
                    # Только фамилия
                    last_name = name_parts[0].strip()
                    query_update = 'UPDATE user_info SET surname = %s WHERE user_discord_id = %s'
                    values = (last_name, user_id)
                elif len(name_parts) == 2:
                    # Фамилия и имя
                    last_name = name_parts[0].strip()
                    first_name = name_parts[1].strip()
                    query_update = 'UPDATE user_info SET surname = %s, name = %s WHERE user_discord_id = %s'
                    values = (last_name, first_name, user_id)
                elif len(name_parts) >= 3:
                    # Фамилия, имя и отчество
                    last_name = name_parts[0].strip()
                    first_name = name_parts[1].strip()
                    middle_name = ' '.join(name_parts[2:]).strip()
                    query_update = 'UPDATE user_info SET surname = %s, name = %s, patronymic = %s WHERE user_discord_id = %s'
                    values = (last_name, first_name, middle_name, user_id)
                else:
                    return JsonResponse({'success': False, 'error': 'Неверный формат ФИО'})

                db.update_value_in_database(query_update, values)
            else:
                # Обновление других полей
                query_update = f'UPDATE user_info SET {field} = %s WHERE user_discord_id = %s'
                db.update_value_in_database(query_update, (value, user_id))

            db.exit_db()
            return JsonResponse({'success': True})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)})
