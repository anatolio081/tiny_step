import json
import os

booking_path = "data/booking.json"
goals_path = "data/goals.json"
teacher_path = "data/teachers.json"
request_path = "data/requests.json"


def get_goals():
    with open(goals_path, "r", encoding='utf-8') as f:
        goals = json.load(f)
    return goals


def get_profiles():
    with open(teacher_path, "r", encoding='utf-8') as f:
        profiles = json.load(f)
    return profiles


def add_order(client_name, client_phone, week_day, client_time, client_teacher):
    order = {"client_name": client_name,
             "client_phone": client_phone,
             "week_day": week_day,
             "time": client_time,
             "teacher_id": client_teacher}
    order_list = []
    if os.path.exists(booking_path):
        with open(booking_path, "r")as f:
            data = f.read()
            order_list = json.loads(data)
    order_list.append(order)
    order_json = json.dumps(order_list, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))
    with open(booking_path, "w")as f:
        f.write(order_json)


def add_request(client_name, client_phone, client_time, goal):
    request = {"client_name": client_name,
               "client_phone": client_phone,
               "time_to_learn": client_time,
               "goal": goal}
    request_list = []
    if os.path.exists(request_path):
        with open(request_path, "r")as f:
            data = f.read()
            request_list = json.loads(data)
    request_list.append(request)
    order_json = json.dumps(request_list, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))
    with open(request_path, "w")as f:
        f.write(order_json)
