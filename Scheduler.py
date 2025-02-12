import builtins

import json
import os
# from datetime import datetime
# import rich
from rich.console import Console

console = Console()
builtins.print = console.print

def create_json_file(filename, data):
    file_path = os.path.join('tasks', filename)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f'FILE CREATED: {file_path}')


while True:
    print('Нажмите [T], чтобы открыть список задач')
    print('Нажмите [C], чтобы открыть календарь')
    print('Нажмите [E], чтобы выйти')
    command1 = input().lower()

    # Вывод списка задач:
    if command1 == 't':
        k = 1
        for json_file in os.listdir('tasks'):
            file_path = os.path.join('tasks', json_file)
            with open(file_path, 'r', encoding='utf-8') as task:
                data = json.load(task)
                task_name = data.get('name')
                task_color = data.get('color', 'white')
                console.print(f"[{task_color}][{k}][/] {task_name}")
            k += 1

        print('\nВведите номер задачи, чтобы открыть подробнее')
        print('[N] - создать новую задачу')
        print('[Back] - вернуться назад')

        # Создание новой задачи, ПОПРАВИТЬ ПОВТОРЫ ЗАДАЧИ
        command = input().lower()
        if command == 'n':
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
            lastJson = os.listdir('tasks')[-1]
            taskNumber = int(lastJson[4:-5]) + 1
            create_json_file('task' + str(taskNumber) + '.json', data)

        elif command.isdigit():
            task_number = os.listdir('tasks')[int(command) - 1]
            file_path = os.path.join('tasks', task_number)

            with open(file_path, 'r', encoding='utf-8') as data:
                data = json.load(data)
                print('Задача:', data['name'])
                print('Тег:', data['tag'])
                print('Описание:', data['description'])
                print('Врем начала:', data['task_begin'])
                print('Дедлайн:', data['deadline'])
                print('Приоритет:', data['priority'])
                if data['repetition'] is True:
                    print(f'Повторять каждые {data["repetition_cooldown"]} дней')
                print('Цвет:', data['color'], '\n')

        elif command == 'back':
            continue

        else:
            print('Неизвестная команда')

    if command1 == 'e':
        break
