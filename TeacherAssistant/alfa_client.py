import datetime
import json

import requests


class AlfaCRMClient:
    def __init__(self, ):
        email = 'maxim.grr.z@gmail.com'
        api_key = '0'
        self.base_url = "https://rtschool.s20.online/v2api"
        self.token = self.authenticate(email, api_key)

    def authenticate(self, email, api_key):
        url = f"{self.base_url}/auth/login"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "api_key": api_key
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            result = response.json()
            raise Exception(f"Authentication failed: {result['name']} - {result['message']}")

        result = response.json()
        print("Authentication successful!")
        return result['token']

    def create_task(self, customer_id, text_task, user_alfa_id, alfa_teacher_id=None, is_tech=False):
        url = f"{self.base_url}/1/task/create"
        headers = {
            "X-ALFACRM-TOKEN": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        assigned_ids = [651]
        if is_tech:
            assigned_ids = [441]
        # assigned_ids = [1844]
        today = datetime.datetime.today() + datetime.timedelta(days=1)
        data = {
            "assigned_ids": assigned_ids,  # ID ответственного лица (651 - Мехавич | 441 - TechSup | 1844 - Test)
            "user_id": user_alfa_id,  # ID пользователя, кто подал
            "branch_ids": [1],  # default - 1
            "customer_ids": customer_id,
            "text": text_task,
            "due_date": today.strftime('%d.%m.%Y')
        }

        # "due_date_time": '23:59'

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            result = response.json()
            raise Exception(f"Task creation failed: {result['name']} - {result['message']}")

        result = response.json()
        task_id = result['model']['id']
        return task_id

    def update_task(self, task_id, new_text):
        url = f"{self.base_url}/1/task/update?id={task_id}"
        headers = {
            "X-ALFACRM-TOKEN": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "text": new_text
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            result = response.json()
            raise Exception(f"Task update failed: {result['name']} - {result['message']}")

        result = response.json()
        return result

    def get_clients(self, page=1):
        url = f"{self.base_url}/1/customer/list"
        headers = {
            "X-ALFACRM-TOKEN": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "page": page,
            "removed": 1  # Только активные
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            result = response.json()
            raise Exception(f"Failed to get clients: {result['name']} - {result['message']}")

        result_clients = response.json()
        return result_clients

    def get_client(self, client_alfa_id):
        url = f"{self.base_url}/1/customer/index"
        headers = {
            "X-ALFACRM-TOKEN": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "id": client_alfa_id,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            result = response.json()
            raise Exception(f"Failed to get clients: {result['name']} - {result['message']}")

        result_clients = response.json()
        return result_clients

    def get_teachers_list(self, page=1):
        url = f'{self.base_url}/1/teacher/index'
        headers = {
            "X-ALFACRM-TOKEN": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "page": page,
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            raise Exception(f"Failed to get clients: {response.status_code}")

        try:
            result_clients = response.json()
            return result_clients
        except json.JSONDecodeError:
            print("Failed to decode JSON:", response.text)
            raise

    def get_teacher(self, alfa_id):
        url = f'{self.base_url}/1/teacher/index'
        headers = {
            "X-ALFACRM-TOKEN": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "id": alfa_id,
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            raise Exception(f"Failed to get clients: {response.status_code}")

        try:
            result_clients = response.json()
            return result_clients
        except json.JSONDecodeError:
            print("Failed to decode JSON:", response.text)
            raise

    def update_client(self, client_id, portfolio_link):
        url = f"{self.base_url}/1/customer/update?id={client_id}"
        headers = {
            "X-ALFACRM-TOKEN": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "custom_portfolio": portfolio_link,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            result = response.json()
            raise Exception(f"Portfolio update failed: {result['name']} - {result['message']}")

        result = response.json()
        return result

    def get_task(self, alfa_object_id):
        url = f"{self.base_url}/1/task/index"
        headers = {
            "X-ALFACRM-TOKEN": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "id": alfa_object_id,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            result = response.json()
            raise Exception(f"Failed to get clients: {result['name']} - {result['message']}")

        result_clients = response.json()
        return result_clients
