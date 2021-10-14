import os
import random

import vk_api as vk
from dotenv import load_dotenv
from google.cloud import dialogflow
from vk_api.longpoll import VkEventType, VkLongPoll


def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=detect_intent_texts('newagent-oqju', event.user_id, event.text, language_code='ru'),
        random_id=random.randint(1,1000)
    )


def main():
    load_dotenv()
    token = os.environ['VK_API_KEY']

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == '__main__':
    main()
