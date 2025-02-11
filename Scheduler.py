import json
import os
from datetime import datetime
import rich

def create_json_file(filename, data):
    f_path = "tasks"
    file_path = os.path.join(f_path, filename)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"FILE CREATED: {file_path}")

data = {
    "tag": "хотелки денчика",
    "name": "Сдать проект",
    "description": "Сдать заявку на инженеры будущего чтоб денчик не убил своим пузом",
    "task_begin": datetime(2025, 2, 10, 12, 00).isoformat() + "Z",
    "deadline": datetime(2025, 2, 14, 19, 00).isoformat() + "Z",
    "priority": 2,
    "repetition": True,
    "repetition_cooldown": 1,
    "color": "red"
}

# create_json_file("task.json", data)

print('Нажмите T, чтобы открыть список задач\n' + 'Нажмите C, чтобы открыть календарь\n')

# Вывод списка задач:
k = 1
if input() == 'T':
    for json_file in os.listdir('tasks'):
        file_path = os.path.join('tasks', json_file)
        with open(file_path, 'r', encoding='utf-8') as task:
            data = json.load(task)
            print(f'{k}.', data.get('name'))
        k += 1
