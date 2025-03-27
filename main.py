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


def looking_for_attempts(timestamp, headers):
    payload = {
        'timestamp': timestamp
    }
    response = requests.get(devman_api_url, headers=headers, params=payload, timeout=90)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.environ['TG_BOT_TOKEN']
    bot = telegram.Bot(tg_token)
    devman_api_url = 'https://dvmn.org/api/long_polling/'
    api_token = os.environ['DEVMAN_TOKEN']
    chat_id = os.environ['CHAT_ID']
    headers = {
        'Authorization': api_token
    }
    timestamp = None
    while True:
        try:
            response = looking_for_attempts(timestamp, headers)
            timestamp = response['last_attempt_timestamp']
            attempts = response['new_attempts']
            for attempt in attempts:
                send_info_about_attempt(attempt, chat_id)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Соединение прервано')
            sleep(10)
