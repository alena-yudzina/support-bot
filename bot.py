import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


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
    text = detect_intent_texts('newagent-oqju', update.effective_chat.id, update.message.text, language_code='ru')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


def main():
    load_dotenv()
    bot_token = os.environ['BOT_TOKEN']
    
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
