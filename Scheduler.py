import builtins
import shutil
import json
import os
from datetime import datetime
# import rich
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
builtins.print = console.print

def create_json_file(filename, data, directory):
    file_path = os.path.join(directory, filename)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f'FILE CREATED: {file_path}')


def check_deadlines():
    for json_file in os.listdir('tasks'):
            file_path = os.path.join('tasks', json_file)
            with open(file_path, 'r', encoding='utf-8') as task:
                data = json.load(task)
                deadlineTimeStr = data.get('deadline').replace('T', ' ').replace('Z', '')
                deadlineTime = datetime.strptime(deadlineTimeStr, '%Y-%m-%d %H:%M:%S')
                nowTimeStr = str(datetime.now())[:-7]
                nowTime = datetime.strptime(nowTimeStr, '%Y-%m-%d %H:%M:%S')
                if deadlineTime < nowTime:
                    print(':exclamation::exclamation::exclamation: [white on red] У ВАС ПРОСРОЧЕН ДЕДЛАААААЙН [/]')


# Создание новой задачи, ПОПРАВИТЬ ПОВТОРЫ ЗАДАЧИ
def create_new_task(directory):
    data = dict()
    data['name'] = input('Название:\n')
    data['tag'] = input('Тег:\n')
    data['description'] = input('Описание:\n')
    data['task_begin'] = input('Время начала:\n')
    data['deadline'] = input('Дедлайн:\n')
    data['priority'] = input('Приоритет (1-3):\n')
    if input('Повторять (ДА или НЕТ):\n').lower() == 'да':
        data['repetition'] = True
        data['repetition_cooldown'] = input('Частота повтора:\n')
    data['color'] = input('Цвет:\n')
    lastJson = os.listdir(directory)[-1]
    taskNumber = int(lastJson[4:-5]) + 1
    create_json_file('task' + str(taskNumber) + '.json', data, directory)

# CheckDeadlines()

while True:
    print('Нажмите [T], чтобы открыть список задач')
    print('Нажмите [C], чтобы открыть календарь')
    print('Нажмите [E], чтобы выйти')
    command1 = input().lower()

# Вывод списка задач:
    if command1 == 't':
        console = Console()
        table = Table(title="===== Задачи =====", expand=True)

        table.add_column("№", justify="right")
        table.add_column("Название")
        table.add_column("Дедлайн", style="green")

        k = 1
        for json_file in os.listdir('tasks'):
            file_path = os.path.join('tasks', json_file)
            with open(file_path, 'r', encoding='utf-8') as task:
                data = json.load(task)
                task_name = data.get('name')
                task_deadline = data.get('deadline', 'N/A')
                task_color = data.get('color', 'white')

                table.add_row(str(f'[{task_color}]{k}[/]'), f'[{task_color}]{task_name}[/]', task_deadline.replace("T", " ").replace("Z", " "))
                k += 1

        print(table)

        print('\nВведите номер задачи, чтобы открыть подробнее')
        print('[N] - создать новую задачу')
        print('[D] - создать новый черновик')
        print('[Back] - вернуться назад')

# Создание новой задачи, ПОПРАВИТЬ ПОВТОРЫ ЗАДАЧИ
        command = input().lower()
        if command == 'n':
            create_new_task('tasks')

# Создание черновика
        elif command == 'd':
            create_new_task('drafts')

# Вывод подробного описания задачи:
        elif command.isdigit():
            task_number = os.listdir('tasks')[int(command) - 1]
            file_path = os.path.join('tasks', task_number)

            with open(file_path, 'r+', encoding='utf-8') as data:
                data = json.load(data)
                table = Table(title=f"===== [1] {data['name']} =====", expand=True)
                table.add_column("№", justify="right")
                table.add_column("Параметр")
                table.add_column("Значение")

                table.add_row("1", "Название", data["name"])
                table.add_row("2", "Тег", data["tag"])
                table.add_row("3", "Описание", data["description"])
                table.add_row("4", "Время начала", data["task_begin"].replace("T", " ").replace("Z", " "))
                table.add_row("5", "Дедлайн", data["deadline"].replace("T", " ").replace("Z", " "))
                table.add_row("6", "Приоритет", str(data["priority"]))
                if data.get("repetition"):
                    table.add_row("7", "Повторение", f"Каждые {data['repetition_cooldown']} дней")
                table.add_row("8", "Цвет", f"[{data['color']}]{data['color']}[/]")
                print(table)
                
                print('Нажмите [R] чтобы отметить как выполненное')
                print('Нажмите [E], чтобы редактировать')
                print('Нажмите [red][D][/], чтобы удалить')
                print('Нажмите [BACK], чтобы выйти')

            command2 = input().lower()

            # Удаление задачи:
            if command2 == 'd': 
                os.remove(file_path)
                print('Задача удалена\n')
                
            # Отметка как выполненное:
            elif command2 == 'r':
                shutil.move(file_path, 'done')
            
            # Изменение задачи:
            elif command2 == 'e':
                n = input('Номер параметра, который хотите изменить: ')
                while n.lower() != 'back':
                    with open(file_path, 'r+', encoding='utf-8') as data:
                        data = json.load(data)
                        if n == '1':
                            data['name'] = input('Название:\n')
                        elif n == '2':
                            data['tag'] = input('Тег:\n')
                        elif n == '3':
                            data['description'] = input('Описание:\n')
                        elif n == '4':
                            data['task_begin'] = input('Время начала:\n')
                        elif n == '5':
                            data['deadline'] = input('Дедлайн:\n')
                        elif n == '6':
                            data['priority'] = input('Приоритет (1-3):\n')
                        elif n == '7':
                            if input('Повторять (ДА или НЕТ):\n') == 'ДА':
                                data['repetition'] = True
                                data['repetition_cooldown'] = input('Частота повтора:\n')
                        elif n == '8':
                            data['color'] = input('Цвет:\n')
                        
                        print('Введите [BACK] чтобы выйти')
                        n = input('Номер параметра, который хотите изменить: ')
                create_json_file(task_number, data)


            elif command2 == 'back':
                continue

        elif command == 'back':
            continue

        else:
            print('Неизвестная команда')

    if command1 == 'e':
        break
