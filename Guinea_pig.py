import telebot
import time
from threading import Thread
import os
from dotenv import load_dotenv
from pytimeparse import parse


load_dotenv("LoginData.env")
TG_TOKEN = os.getenv('tg_token')
bot = telebot.TeleBot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=20, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def timer(chat_id, seconds):
    fulltime = seconds
    progress = 0
    progressbar = render_progressbar(
        fulltime, progress, prefix='', suffix='', length=20, fill='█', zfill='░')
    sent_message = bot.send_message(
        chat_id, f'Осталось {seconds} с\n {progressbar}')
    while seconds:
        time.sleep(1)
        seconds -= 1
        progress += 1
        progressbar = render_progressbar(
            fulltime, progress, prefix='', suffix='', length=20, fill='█', zfill='░')
        bot.edit_message_text(
            f'Осталось {seconds} с\n {progressbar}', chat_id, sent_message.message_id)
    bot.send_message(chat_id, 'Время вышло!')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, '''Привет! Для запуска таймера используйте команду /timer <время>.
Время нужно указать с единицами измерения (s, m, h), 
например: /timer 10s''')


@bot.message_handler(commands=['timer'])
def set_timer(message):
    try:
        set_time = message.text.split()[1]
        seconds = int(parse(set_time))
        chat_id = message.chat.id
        bot.send_message(chat_id, f'Устанавливаю таймер на {set_time}')
        Thread(target=timer, args=(chat_id, seconds)).start()
    except (IndexError, ValueError, TypeError):
        bot.send_message(
            message.chat.id, 'Неверный формат времени')
        bot.send_message(
            message.chat.id, 'Время указывается с единицами измерения, например: /timer 10s')


@bot.message_handler(func=lambda message: True)
def handle_all_other_messages(message):
    bot.reply_to(message, 'Я отвечаю только на /start и /timer')
    bot.send_message(
        message.chat.id, '''Для запуска таймера используйте команду /timer <время>. 
Время нужно указать с единицами измерения (s, m, h), 
например: /timer 10s''')


def main():
    bot.polling()


if __name__ == '__main__':
    main()

























