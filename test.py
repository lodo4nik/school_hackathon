import os
import json
from datetime import datetime
import shutil

def CheckDeadlines():
    for json_file in os.listdir('tasks'):
            file_path = os.path.join('tasks', json_file)
            with open(file_path, 'r+', encoding='utf-8') as task:
                data = json.load(task)
                deadlineTimeStr = data.get('deadline').replace('T', ' ').replace('Z', '')
                deadlineTime = datetime.strptime(deadlineTimeStr, '%Y-%m-%d %H:%M:%S')
                nowTimeStr = str(datetime.now())[:-7]
                nowTime = datetime.strptime(nowTimeStr, '%Y-%m-%d %H:%M:%S')
                if deadlineTime < nowTime:
                    print('У ВАС ПРОСРОЧЕН ДЕДЛАААААЙН')
                    status = input('Вы выполнили задачу?(сосали?) Да/Нет: ')
                    if status.lower() == 'да':
                        data['done'] = True
                        json_file.seek(0)
                        print(data)
                        json.dump(data, json_file)
                        # shutil.move('tasks', 'done')
                        

CheckDeadlines()