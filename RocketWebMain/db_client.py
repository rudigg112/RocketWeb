import mysql.connector
import datetime
import json

class DBClient:
    def __init__(self):

        dbconfig = {
            'host': '',
            'user': 'root',
            'password': '&',
            'database': 'rocket_buddy',
        }

        self.conn = mysql.connector.connect(**dbconfig)
        self.cursor = self.conn.cursor()
        timezone_offset = +3.0
        tzinfo = datetime.timezone(datetime.timedelta(hours=timezone_offset))
        self.date_now = datetime.datetime.now(tzinfo).date()

    def exit_db(self):
        self.cursor.close()
        self.conn.close()

    def select_fetchall(self, query_select_fetchall, values=()):
        self.cursor.execute(query_select_fetchall, values)
        result = self.cursor.fetchall()
        self.conn.commit()

        return result

    def select_fetchone(self, query_select_fetchone, values=()):
        self.cursor.execute(query_select_fetchone, values)
        result = self.cursor.fetchone()
        self.conn.commit()

        return result

    def update_value_in_database(self, query_update, values=()):
        self.cursor.execute(query_update, values)
        self.conn.commit()

    def insert_object_in_database(self, query_insert, values=()) -> int:
        self.cursor.execute(query_insert, values)
        self.conn.commit()

        last_row_id = int(self.cursor.lastrowid)
        return last_row_id

    def delete_object_in_database(self, query_delete, values=()):
        self.cursor.execute(query_delete, values)
        self.conn.commit()

    def execute_many(self, query_execute_many, values):
        print(query_execute_many, values)
        self.cursor.executemany(query_execute_many, values)
        self.conn.commit()

    def load_draft(self, teacher_id, client_link=None, task_id=None):
        if client_link:
            _sql = (
                'SELECT id, well, video_link, theme_number, project_type, project_name, project_description, skils, '
                'lessons_count, date_created, type_lesson '
                'FROM tasks_teacher WHERE teacher_id = %s AND client_link = %s AND is_complete = 0')
            result = self.select_fetchone(_sql, (teacher_id, client_link))
        else:
            _sql = (
                'SELECT id, well, video_link, theme_number, project_type, project_name, project_description, skils, '
                'lessons_count, date_created, type_lesson '
                'FROM tasks_teacher WHERE id = %s')
            result = self.select_fetchone(_sql, (task_id,))

        return result

    def create_draft(self, user_id, client_link, client_name, client_age, client_portfolio,
                     client_country, client_market, tl_name, client_id, formate_lesson, parts, student_gender):
        print('db_ create_draft', user_id, client_link, client_name, client_age, client_portfolio,
              client_country, client_market, tl_name, client_id)
        _sql = ('INSERT INTO tasks_teacher (teacher_id, client_link, student_name, student_age, portfolio, '
                'country, market, tl_name, client_alfa_id, rc_accrual, student_gender) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        obj_id = self.insert_object_in_database(_sql, (user_id, client_link, client_name, client_age,
                                                       client_portfolio, client_country,
                                                       client_market, tl_name, client_id, json.dumps(parts), student_gender))

        return obj_id

    def update_draft_field(self, task_id, field, value):
        _sql = 'UPDATE tasks_teacher SET {} = %s WHERE id = %s'.format(field)
        self.update_value_in_database(_sql, (value, task_id))

    def complete_task(self, task_id):
        _sql = 'UPDATE tasks_teacher SET is_complete = 1 WHERE id = %s'
        self.update_value_in_database(_sql, (task_id,))

    def check_profile(self, username, user_id) -> None:
        query = 'SELECT id FROM user WHERE user_id = %s'
        result = self.select_fetchone(query, (user_id,))

        if not result:
            query_insert = 'INSERT INTO user (username, user_id) VALUES (%s, %s)'
            obj_id = self.insert_object_in_database(query_insert, (username, user_id))
        else:
            obj_id = result[0]

        query_select_info = 'SELECT id FROM user_info WHERE user_obj_id = %s'
        result_obj = self.select_fetchone(query_select_info, (obj_id,))

        if not result_obj:
            query_insert_info_obj = 'INSERT INTO user_info (user_obj_id, user_discord_id) ' \
                                    'VALUES (%s, %s)'
            self.insert_object_in_database(query_insert_info_obj, (obj_id, user_id))

    def get_language(self, discord_id):
        query = 'SELECT language FROM user WHERE user_id = %s'
        try:
            result = self.select_fetchone(query, (discord_id,))[0]
            lang = result
        except Exception as ex:
            lang = 'eng'
            print(f'Error [DB:get_language] | {ex}')

        return lang