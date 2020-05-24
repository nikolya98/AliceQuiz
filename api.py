from __future__ import unicode_literals
import json
import logging
from flask import Flask, request
from quiz import get_themes, thematic_quiz, difficult_quiz
import time
import random


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
sessionStorage = {}


app.route("/", methods=['POST'])


def main():
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
    # Новый пользователь: Инициализация, приветствие, предлагаем сыграть...
    user_id = req['session']['user_id']
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Да",
                "Нет",
            ]
        }
        res['response']['text'] = 'Привет! Сыграем?'
        res['response']['buttons'] = get_suggests(user_id)
        return
    # Пользователь согласился
    if req['request']['original_utterance'].lower() in [
        'сыграем',
        'да',
        'ок',
        'го',
    ]:
        # Играет, пока не надоест...
        while True:
            # Предлагаем выбор режима игры...
            sessionStorage[user_id] = {
                'suggests': [
                    "Викторина по темам",
                    "Режим Всезнайка"
                ]
            }
            res['response']['text'] = 'Выберите режим игры.'
            res['response']['buttons'] = get_suggests(user_id)
            yield

            # Пользоватеь выбрал тематическую викторину
            if req['request']['original_utterance'].lower() in [
                'виторина по темам',
                'тематическая'
            ]:
                themes = get_themes('thematic')
                sessionStorage[user_id] = {
                    'suggests': themes
                }
                # Пользователь должен корректно ввести тему викторины...
                while True:
                    res['response']['text'] = 'Выберите тему'
                    res['response']['buttons'] = get_suggests(user_id)
                    yield

                    if req['request']['original_utterance'].lower() not in [i.lower() for i in themes]:
                        res['response']['text'] = 'Нет такой темы, попробуйте ещё раз!'
                        continue
                    else:
                        chosen_theme = req['request']['original_utterance'].capitalize()
                        break
                # Счётчики верных ответов и времени игры...
                good_attempts = 0
                start = time.time()
                # На каждой итерации получаем кортеж (Вопрос, [Список вариантов ответа], Правильный ответ)
                for i in thematic_quiz(chosen_theme):
                    question, prompts, answer = i
                    prompts = random.shuffle(prompts)
                    res['response']['text'] = question
                    sessionStorage[user_id] = {
                        'suggests': prompts
                    }
                    res['response']['buttons'] = get_suggests(user_id)
                    if req['request']['original_utterance'].lower() == answer.lower():
                        good_attempts += 1

            # Пользователь выбрал режим "Всезнайка"...
            if req['request']['original_utterance'].lower() == 'всезнайка':
                res['response']['text'] = 'Итак, поехали!'
                good_attempts = 0
                start = time.time()
                for i in difficult_quiz():
                    question, answer = i
                    res['response']['text'] = question
                    if req['request']['original_utterance'].lower() == answer.lower():
                        good_attempts += 1
                    elif req['request']['original_utterance'].lower() in answer.lower():
                        good_attempts += 1
                    res['response']['text'] = f'Правильный ответ: {answer}'

            # Выводим результаты игры и предлагаем сыграть ещё раз
            spend_time = time.time() - start
            res['response']['text'] = f'Ответов угадано: {good_attempts}'
            res['response']['text'] = f'Времени потрачено: {spend_time}'
            res['response']['text'] = 'Сыграем ещё раз?'
            if req['request']['original_utterance'].lower() in [
                'да',
                'сыграем',
                'ещё раз'
            ]:
                continue
            if req['request']['original_utterance'].lower() in [
                'нет',
                'отстань',
                'мне пора',
                'не хочу'
            ]:
                break

    # Пользователь отказался...
    else:
        res['response']['text'] = 'Всего хорошего!'
        return


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests_start']
    ]
    return suggests
