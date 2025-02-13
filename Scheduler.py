import builtins
import shutil
import json
import os
from datetime import datetime, timedelta
import calendar
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
builtins.print = console.print

# СОЗДАНИЕ ЖСОН ФАЙЛА, вроде работает
def create_json_file(filename, data, directory):
    file_path = os.path.join(directory, filename)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f'FILE CREATED: {file_path}')

# ПРОВЕРКА ДЕДЛАЙНОВ, я ниче не менял мне страшно вообще сюда заходить
def check_deadlines():
    for json_file in os.listdir('tasks'):
        file_path = os.path.join('tasks', json_file)
        flag = False
        fp = ''
        with open(file_path, 'r+', encoding='utf-8') as task:
            fp = file_path
            data = json.load(task)
            taskName = data.get('name')
            deadlineTimeStr = data.get('deadline').replace('T', ' ').replace('Z', '')
            deadlineTime = datetime.strptime(deadlineTimeStr, '%Y-%m-%d %H:%M:%S')
            nowTimeStr = str(datetime.now())[:-7]
            nowTime = datetime.strptime(nowTimeStr, '%Y-%m-%d %H:%M:%S')
            if deadlineTime < nowTime:
                command = Prompt.ask(f'[white on red] Просрочен дедлайн -> [/] [red]{taskName}[/] | Вы выполнили задачу? Да/Нет').lower()
                if command == 'да':
                    flag = True
                    data['done'] = 'true'
                    print("[black on green] Записано [/]")
                    with open(file_path, 'w', encoding='utf-8') as task1:
                        json.dump(data, task1, ensure_ascii=False, indent=2)
        # if flag == True:
            #shutil.move(fp, 'done')

# КАЛЕНДАРЬ
def show_calendar():
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day

    first_day = datetime(current_year, current_month, 1)
    first_weekday = first_day.weekday()
    month_days = calendar.monthrange(current_year, current_month)[1]

    days = []
    days += [''] * first_weekday
    for day in range(1, month_days + 1):
        days.append(day)
    while len(days) % 7 != 0:
        days.append('')

    colors = {}

    for json_file in os.listdir('tasks'):
        file_path = os.path.join('tasks', json_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            task_begin = data.get('task_begin', '')
            deadline = data.get('deadline', '')
            color = data.get('color', 'white')

            task_begin = datetime.strptime(task_begin.replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')
            deadline = datetime.strptime(deadline.replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')

            start_date = task_begin.date()
            end_date = deadline.date()

            if start_date > end_date:
                continue

            current_day = start_date
            while current_day <= end_date:
                if current_day.month == current_month and current_day.year == current_year:
                    day_number = current_day.day
                    colors[day_number] = color
                current_day += timedelta(days=1)

    table = Table(title=f"Календарь {first_day.strftime('%B %Y')}", show_header=True, expand=True)
    for day_name in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        table.add_column(day_name, justify="center")

    weeks = [days[i:i+7] for i in range(0, len(days), 7)]

    for week in weeks:
        row_elements = []
        for day in week:
            if day == '':
                row_elements.append('')
                continue
            day_color = colors.get(day)
            text = f"{day}"
            text = f"[black on {day_color}]{text}[/]"
            row_elements.append(text)
        table.add_row(*row_elements)

    console.print(table)

# СОЗДАНИЕ НОВОЙ ЗАДАЧИ
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

    command1 = input().lower()
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
    command = input().lower()
    if command == 'd':
        os.remove(file_path)
        print('Задача удалена\n')
    elif command == 'r':
        data['done'] = 'true'
        print("[black on green] Записано [/]")
        with open(file_path, 'w', encoding='utf-8') as task1:
            json.dump(data, task1, ensure_ascii=False, indent=2)
    elif command == 'e':
        n = input('Номер параметра, который хотите изменить: ')
        while n.lower() != 'back':
            with open(file_path, 'r+', encoding='utf-8') as f:
                data = json.load(f)
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
                if input('Повторять (ДА или НЕТ):\n').lower() == 'да':
                    data['repetition'] = True
                    data['repetition_cooldown'] = input('Частота повтора:\n')
            elif n == '8':
                data['color'] = input('Цвет:\n')
            print('Введите [BACK] чтобы выйти')
            n = input('Номер параметра, который хотите изменить: ')
        create_json_file(task_file, data, 'tasks')
    elif command == 'back':
        return

# СПИСОК ЗАДАЧ
def tasks_menu():
    while True:
        console = Console()
        table = Table(title="===== Задачи =====", expand=True)
        table.add_column("№", justify="right")
        table.add_column("Название")
        table.add_column("Дедлайн", style="green")
        task_files = os.listdir('tasks')
        if not task_files:
            print("Нет задач")
        k = 1
        for task_file in task_files:
            file_path = os.path.join('tasks', task_file)
            with open(file_path, 'r', encoding='utf-8') as task:
                data = json.load(task)
                task_name = data.get('name')
                task_deadline = data.get('deadline', 'N/A')
                task_color = data.get('color', 'white')
                task_status = data.get('done', 'false')
                if task_status == "true":
                    table.add_row(f'[{task_color}]{k}[/]', f'[{task_color}]{task_name}[/]', task_deadline.replace("T", " ").replace("Z", " "), style="strike")
                else:
                    table.add_row(f'[{task_color}]{k}[/]', f'[{task_color}]{task_name}[/]', task_deadline.replace("T", " ").replace("Z", " "))
            k += 1
        print(table)
        print('\nВведите номер задачи, чтобы открыть подробнее')
        print('[N] - создать новую задачу')
        print('[D] - создать новый черновик')
        print('[Back] - вернуться в главное меню')
        command = input().lower()
        if command == 'back':
            break
        elif command == 'n':
            create_new_task('tasks')
        elif command == 'd':
            create_new_task('drafts')
        elif command.isdigit():
            idx = int(command) - 1
            if 0 <= idx < len(task_files):
                open_task_detail(task_files[idx])
            else:
                print("Неверный номер задачи")
        else:
            print("Неизвестная команда")

# ШЛЯПА ПОД КАЛЕНДАРЕМ. на будущее, вдруг сам календарь вообще можно будет перенести в главное меню и что нибудь с ним сделать
# ну или сделать больше действий с календарем
def calendar_menu():
    while True:
        show_calendar()
        # здесь надо будет что нибудь придумать с переходами по датам
        # можно сделать функцию, которая показывает список задач на определеннный день
        # и тогда в главном меню показывать просто вывод этой функции для сегодняшнего дня
        print('[Back] - вернуться в главное меню')
        command = input().lower()
        if command == 'back':
            break
        else:
            print("Неизвестная команда")

# ГЛАВНОЕ МЕНЮ
def main_menu():
    while True:
        print('Нажмите [T], чтобы открыть список задач')
        print('Нажмите [C], чтобы открыть календарь')
        print('Нажмите [E], чтобы выйти')
        command = input().lower()
        if command == 't':
            tasks_menu()
        elif command == 'c':
            calendar_menu()
        elif command == 'e':
            break
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    check_deadlines()
    main_menu()