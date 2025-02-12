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
# create_json_file("task.json", data)

print('Нажмите T, чтобы открыть список задач\n' + 'Нажмите C, чтобы открыть календарь\n')

# Вывод списка задач:
if input() == 'T':
    k = 1
    for json_file in os.listdir('tasks'):
        file_path = os.path.join('tasks', json_file)
        with open(file_path, 'r', encoding='utf-8') as task:
            data = json.load(task)
            print(f'{k}.', data.get('name'))
        k += 1
    print('Введите номер задачи, чтобы открыть подробнее\n' + 'Нажмите N, чтобы создать новую задачу\n')

# Создание новой задачи, ПОПРАВИТЬ ПОВТОРЫ ЗАДАЧИ

    if input() == 'N':
        data = dict()
        data['name'] = input('Название:\n')
        data['tag'] = input('Тег:\n')
        data['description'] = input('Описание:\n')
        data['task_begin'] = input('Время начала:\n')
        data['deadline'] = input('Дедлайн:\n')
        data['priority'] = input('Приоритет (1-3):\n')
        if input('Повторять (ДА или НЕТ):\n') == 'ДА':
            data['repetition'] = True
            data['repetition_cooldown'] = input('Частота повтора:\n')
        data['color'] = input('Цвет:\n)')

        create_json_file("task.json", data)

