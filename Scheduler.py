import json
import os
from datetime import datetime

def create_json_file(filename, data):
    f_path = "tasks"
    fi_path = os.path.join(f_path, filename)

    with open(fi_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    
    print(f"FILE CREATED: {fi_path}")

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

create_json_file("task.json", data)
