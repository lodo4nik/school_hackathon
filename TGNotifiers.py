from notifiers import get_notifier
import time
import notifiers

token = '7389744325:AAGKqUPIj3vNGvLS-QtMLK5t-KV8DjUeDws'
chat_id = 1937547931
Flag = True

def send_nots(message):
    telegram = get_notifier('telegram')
    message_text = message
    telegram.notify(message=message_text, token=token, chat_id=chat_id)


while Flag:
        message = input("\nВведите сообщение.\nДля выхода введите e.\n>>>")
        if message.lower() == "e":
            print("Завершение работы")
            Flag = False
        
        else:
            timer = int(input("Введите через сколько минут отправить уведомление\n>>>"))*60
            print(f"Сообщение будет отправлено через {timer//60} минут\n")
            time.sleep(timer)
            send_nots(message)
