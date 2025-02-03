import json
import traceback

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from RocketWebMain.db_client import DBClient
from TeacherAssistant.alfa_client import AlfaCRMClient


@csrf_exempt
def check_client(request):
    if request.method == 'GET':
        print(request.GET.get('type'))
        client_id = request.GET.get('client_id')
        db = DBClient()

        # Проверяем, существует ли запись с указанным client_id
        query_check = """
        SELECT id, is_complete FROM tasks_teacher 
        WHERE client_link = %s AND teacher_id = %s
        """
        result = db.select_fetchone(
            query_check,
            (f'https://rtschool.s20.online/company/1/customer/view?id={client_id}', request.user.discord_id)
        )

        db.exit_db()

        if result:
            task_id, is_complete = result
            return JsonResponse({'success': True, 'task_id': task_id, 'is_complete': bool(is_complete)})
        else:
            return JsonResponse({'success': False})  # Запись не найдена


@csrf_exempt
def update_task_defense_field(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            field = data.get('field')
            value = data.get('value')

            if not task_id or not field or value is None:
                return JsonResponse({'success': False, 'error': 'Не все данные предоставлены'})

            db = DBClient()

            # Обновляем данные в базе данных
            query_update = f'UPDATE tasks_teacher SET {field} = %s WHERE id = %s'
            db.update_value_in_database(query_update, (value, task_id))

            db.exit_db()
            return JsonResponse({'success': True})
        except Exception as e:
            traceback.print_exc()
            print(e)
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def create_draft(request):
    if request.method == 'POST':
        try:
            alfa = AlfaCRMClient()

            data = json.loads(request.body)
            client_id = data.get('client_id')
            user_id = data.get('user_id')

            db = DBClient()

            # Получаем информацию о клиенте и учителе
            teacher_info = alfa.get_teacher(
                db.select_fetchone('SELECT alfa_teacher_id FROM user_info WHERE user_discord_id = %s', (user_id,))[0]
            )
            tl_name = teacher_info['items'][0]['custom_teacherteamlead'][0] if teacher_info[
                                                                                   'total'] == 1 else 'Not found'

            client_info = alfa.get_client(client_id)
            client_items = client_info['items'][0]
            client_name = client_items['custom_childname']
            client_age = client_items['custom_age']
            client_country = client_items['custom_strana']
            client_market = client_items['custom_market']
            client_portfolio = client_items['custom_portfolio']
            formate_lesson = client_items['custom_formatofpaidlessons']
            student_gender = client_items['custom_studentgender']
            parts = {'parts': []}

            # Создаем новую запись
            task_id = db.create_draft(
                user_id=user_id,
                client_link=f'https://rtschool.s20.online/company/1/customer/view?id={client_id}',
                client_name=client_name,
                client_age=client_age,
                client_portfolio=client_portfolio,
                client_country=client_country,
                client_market=client_market,
                tl_name=tl_name,
                client_id=client_id,
                formate_lesson=formate_lesson,
                parts=parts,
                student_gender=student_gender
            )

            db.exit_db()

            return JsonResponse({'success': True, 'task_id': task_id})
        except Exception as e:
            print(f'Error [create_draft]: {e}')
            return JsonResponse({'success': False, 'error': str(e)})


def certificate(request):
    return render(request, 'TeachersAssistant/certificate_task_listing.html')


def certificate_task(request, task_id):
    return render(request, 'TeachersAssistant/certificate_task.html')


def gifts(request):
    return render(request, 'TeachersAssistant/gifts_task_listing.html')


def gifts_task(request):
    return render(request, 'TeachersAssistant/gifts_task.html')


def support(request):
    return render(request, 'TeachersAssistant/support_task_listing.html')


def support_task(request):
    return render(request, 'TeachersAssistant/support_task.html')


def portfolio(request):
    return render(request, 'TeachersAssistant/portfolio_task_listing.html')


def portfolio_task(request):
    return render(request, 'TeachersAssistant/portfolio_task.html')


def project_defense(request):
    if request.user.is_authenticated:
        db = DBClient()
        print('соединение', db)

        _sql = 'SELECT id, client_link, is_complete FROM tasks_teacher WHERE teacher_id = %s'
        result = db.select_fetchall(_sql, (request.user.discord_id,))
        print(result, request.user.discord_id)
        db.exit_db()

        # Форматируем данные для удобного использования в шаблоне
        tasks = []
        for task in result:
            task_id, client_link, is_complete = task
            status = "Отправлено" if is_complete else "Не отправлено"
            tasks.append({
                'id': task_id,
                'client_link': client_link,
                'status': status,
                'is_complete': is_complete
            })

        data = {
            'tasks': tasks
        }

        return render(request, 'TeachersAssistant/defense_task_listing.html', data)
    return redirect('/login')


def project_defense_task(request, task_id):
    db = DBClient()

    _sql = ('SELECT id, teacher_id, tl_name, client_link, client_alfa_id, well, video_link, theme_number, '
            'project_type, project_name, project_description, skils, lessons_count, is_complete, date_created, '
            'type_lesson, expert, expert_review, rc_accrual_1, rc_accrual_2, rc_accrual_3, student_name, '
            'student_age, student_gender, portfolio, language_lesson, country, market, alfa_object_id, '
            'message_task_link, rc_accrual, datetime_send, datetime_review, date_lesson FROM tasks_teacher WHERE id = %s')
    result = db.select_fetchone(_sql, (task_id,))

    _sql = 'SELECT alfa_id, alfa_teacher_id FROM user_info WHERE user_discord_id = %s'
    alfa_id, alfa_teacher_id = db.select_fetchone(_sql, (request.user.discord_id,))

    (task_id, teacher_id, tl_name, client_link, client_alfa_id, well, video_link, theme_number,
     project_type, project_name, project_description, skills, lessons_count, is_complete, date_created,
     type_lesson, expert, expert_review, rc_accrual_1, rc_accrual_2, rc_accrual_3, student_name,
     student_age, student_gender, portfolio, language_lesson, country, market, alfa_object_id,
     message_task_link, rc_accrual, datetime_send, datetime_review, date_lesson) = result


    db.exit_db()

    data = {
        'task_info': {
            'task_id': task_id,
            'teacher_id': teacher_id,
            'tl_name': tl_name,
            'client_link': client_link,
            'client_alfa_id': client_alfa_id,
            'well': well,
            'video_link': video_link,
            'theme_number': theme_number,
            'project_type': project_type,
            'project_name': project_name,
            'project_description': project_description,
            'skills': skills,
            'lessons_count': lessons_count,
            'is_complete': is_complete,
            'date_created': date_created,
            'type_lesson': type_lesson,
            'expert': expert,
            'expert_review': expert_review,
            'rc_accrual_1': rc_accrual_1,
            'rc_accrual_2': rc_accrual_2,
            'rc_accrual_3': rc_accrual_3,
            'student_name': student_name,
            'student_age': student_age,
            'student_gender': student_gender,
            'portfolio': portfolio,
            'language_lesson': language_lesson,
            'country': country,
            'market': market,
            'alfa_object_id': alfa_object_id,
            'message_task_link': message_task_link,
            'rc_accrual': rc_accrual,
            'datetime_send': datetime_send,
            'datetime_review': datetime_review,
            'date_lesson': date_lesson,
            'alfa_id': alfa_id,
            'alfa_teacher_id': alfa_teacher_id,


        }
    }

    return render(request, 'TeachersAssistant/defence_task.html', data)
