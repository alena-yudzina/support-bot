import logging
import os

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте!'
    )


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
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
