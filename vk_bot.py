import logging
import os
import random

import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from intent_converter import detect_intent_texts
from logger import TelegramLogsHandler


logger = logging.getLogger('Logger')


def send_answer(event, vk_api, dialogflow_project_id):
    message = detect_intent_texts(dialogflow_project_id, f'vk_{event.user_id}', event.text, language_code='ru')
    if message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1,1000)
        )


def main():
    load_dotenv()
    token = os.environ['VK_API_KEY']
    dialogflow_project_id = os.environ['PROJECT_ID']
    log_bot_token = os.environ['LOG_BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']

    log_bot = telegram.Bot(token=log_bot_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                send_answer(event, vk_api, dialogflow_project_id)
            except Exception:
                logger.exception('Проблема:')


if __name__ == '__main__':
    main()
