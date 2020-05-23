from __future__ import unicode_literals
import json
import logging
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
sessionStorage = {} # Хранилище данных о сессиях.


app.route("/", methods=['POST'])


def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(request.json, response)
    logging.info('Response: %r', response)
    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle_dialog(req, res):
    # Функция для непосредственной обработки диалога.
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.

        sessionStorage[user_id] = {
            'suggests': [
                "..."
            ]
        }

        res['response']['text'] = 'Привет!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        '...'
    ]:
        res['response']['text'] = '...'
        return

    res['response']['text'] = '...' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    # Функция возвращает подсказки для ответа.
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests
