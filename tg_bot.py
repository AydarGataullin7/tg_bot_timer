import os
import ptbot
import pytimeparse
from dotenv import load_dotenv
from pytimeparse import parse
from decouple import config


load_dotenv()
TG_TOKEN = config('TG_TOKEN')
TG_CHAT_ID = config('TG_CHAT_ID')


def make_wait(bot):
    def wait(chat_id, message):
        seconds = parse(message)
        message_id = bot.send_message(
            chat_id, "Таймер установлен на: {0} секунд".format(seconds))
        bot.create_countdown(seconds, make_notify_progress(bot),
                             chat_id=chat_id, message_id=message_id, total_seconds=seconds)
        bot.create_timer(seconds + 0.1, make_answer(bot), chat_id=chat_id)
    return wait


def make_notify_progress(bot):
    def notify_progress(secs_left, chat_id, message_id, total_seconds):
        progressbar = render_progressbar(
            total_seconds, total_seconds - secs_left)
        progress_message = "Осталось секунд: {0}\n{1}".format(
            secs_left, progressbar)
        bot.update_message(chat_id, message_id, progress_message)
    return notify_progress


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def make_answer(bot):
    def answer(chat_id):
        answer_text = "Время вышло!"
        bot.send_message(chat_id, answer_text)
    return answer


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(make_wait(bot))
    bot.run_bot()


if __name__ == '__main__':
    main()
