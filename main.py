import os
import requests
from dotenv import load_dotenv
from pprint import pprint
import telegram
import argparse


load_dotenv()


tg_token = os.environ['TG_BOT_TOKEN']
bot = telegram.Bot(tg_token)
url='https://dvmn.org/api/long_polling/'
API_TOKEN = os.environ['DEVMAN_TOKEN']
headers = {
    'Authorization': API_TOKEN
}


def send_info_about_attempt(attempt, chat_id):
    if attempt['is_negative']:
        bot.send_message(chat_id, f'''У вас проверили задание с урока 
{attempt['lesson_title']} 
({attempt['lesson_url']})\n
К сожалению, в работе нашлись ошибки.''')
    else:
        bot.send_message(chat_id, f'''У вас проверили задание с урока 
{attempt['lesson_title']} 
({attempt['lesson_url']})\n
Работа принята, можно продолжать!''')


def looking_for_attempts(timestamp, url, headers):
    payload = {
        'timestamp': timestamp
    }
    response = requests.get(url, headers=headers, params=payload, timeout=5)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='devman_tg_bot',
        description='''Send notifications about finishing of 
        checking in Devman site by Telegram bot''')
    parser.add_argument('chat_id',
                        help='Input your Telegram chat id here')
    args = parser.parse_args()


    timestamp=None
    while True:
        try:
            response = looking_for_attempts(timestamp, url, headers)
            timestamp = response['last_attempt_timestamp']
            attempts = response['new_attempts']
            for attempt in attempts:
                send_info_about_attempt(attempt, args.chat_id)
        except requests.exceptions.ReadTimeout:
            print('Работ нет')
        except requests.exceptions.ConnectionError:
            print('Соединение прервано')
