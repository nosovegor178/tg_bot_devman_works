import os
import requests
from dotenv import load_dotenv
import telegram
from time import sleep


def send_info_about_attempt(attempt, chat_id):
    if attempt['is_negative']:
        bot.send_message(chat_id, f'''У вас проверили задание с урока
"{attempt['lesson_title']}"
({attempt['lesson_url']})\n
К сожалению, в работе нашлись ошибки.''')
    else:
        bot.send_message(chat_id, f'''У вас проверили задание с урока
"{attempt['lesson_title']}"
({attempt['lesson_url']})\n
Работа принята, можно продолжать!''')


def looking_for_attempts(timestamp, url, headers):
    payload = {
        'timestamp': timestamp
    }
    response = requests.get(url, headers=headers, params=payload, timeout=90)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    TG_TOKEN = os.environ['TG_BOT_TOKEN']
    bot = telegram.Bot(TG_TOKEN)
    URL = 'https://dvmn.org/api/long_polling/'
    API_TOKEN = os.environ['DEVMAN_TOKEN']
    CHAT_ID = os.environ['CHAT_ID']
    headers = {
        'Authorization': API_TOKEN
    }
    timestamp = None
    while True:
        try:
            response = looking_for_attempts(timestamp, URL, headers)
            timestamp = response['last_attempt_timestamp']
            attempts = response['new_attempts']
            for attempt in attempts:
                send_info_about_attempt(attempt, CHAT_ID)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Соединение прервано')
            sleep(10)
