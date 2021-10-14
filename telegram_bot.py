import logging
import os

import telegram
from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram.ext import (CommandHandler, Filters,
                          MessageHandler, Updater)

logger = logging.getLogger('Logger')

class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте!'
    )


def echo(update, context):
    # Не понимаю, как перенести ключ в main
    dialogflow_project_id = os.environ['PROJECT_ID']
    try:
        text = detect_intent_texts(dialogflow_project_id, update.effective_chat.id, update.message.text, language_code='ru')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text
        )
    except Exception:
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

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
