from notifiers import get_notifier
import requests
import json


token = '7389744325:AAGKqUPIj3vNGvLS-QtMLK5t-KV8DjUeDws'
url = f'https://api.telegram.org/bot{token}/getUpdates'
Flag = True
response = requests.get(url).json()


data = {}
for update in response['result']:
    if 'message' in update:
        # username = update['message']['from'].get('username')
        # print(f"Username: {username}, Chat ID: {chat_id}")
        chat_id = update['message']['chat']['id']
        data[chat_id] = list()

        with open("tgUsers.json", "w") as f:
            f.write(json.dumps(data, indent=4))

def send_nots(message):
    telegram = get_notifier('telegram')
    message_text = message
    telegram.notify(message=message_text, token=token, chat_id=chat_id)



# while Flag:
#         message = input("\nВведите сообщение.\nДля выхода введите e.\n>>>")
#         if message.lower() == "e":
#             print("Завершение работы")
#             Flag = False
        
#         else:
#             timer = int(input("Введите через сколько минут отправить уведомление\n>>>"))*60
#             print(f"Сообщение будет отправлено через {timer//60} минут\n")
#             time.sleep(timer)
#             send_nots(message)
