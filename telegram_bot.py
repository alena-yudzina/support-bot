import logging
import os

import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from intent_converter import detect_intent_texts
from logger import TelegramLogsHandler

logger = logging.getLogger('Logger')


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте!'
    )


def send_answer(update, context):

    dialogflow_project_id = context.bot_data['project_id']
    text = detect_intent_texts(dialogflow_project_id, update.effective_chat.id, update.message.text, language_code='ru')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )
    logger.exception('Проблема:')


def main():
    load_dotenv()
    bot_token = os.environ['BOT_TOKEN']
    log_bot_token = os.environ['LOG_BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    
    log_bot = telegram.Bot(token=log_bot_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['project_id'] = os.environ['PROJECT_ID']

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), send_answer))
    dispatcher.add_error_handler(TelegramLogsHandler(log_bot, chat_id))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
