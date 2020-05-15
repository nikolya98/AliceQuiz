import sqlite3
import random
import time
from db_create import create_thematic_db, create_difficult_db


def thematic_quiz():
    create_thematic_db()
    db = sqlite3.connect('data_bases/thematic_quiz.db')
    sql = db.cursor()

    sql.execute(f"""SELECT name FROM sqlite_master WHERE type = 'table'""")
    tables_name = sql.fetchall()
    themes = []
    for name in tables_name:
        for elem in name:
            themes.append(elem)

    choose_theme = random.sample(themes, 2)  # Предлагаем тему на выбор.... Добавить больше тем для викторин!!!
    for theme in themes:
        print(f'{themes.index(theme) + 1}. {theme}')

    while True:
        user_choice = input('Выберите тему: ')  # Переменная для выбора пользователя...
        if user_choice in choose_theme:
            break
        else:
            print('Такой темы нет! Выберите из списка....')

    sql.execute(f"""SELECT * FROM {user_choice} ORDER BY RANDOM() LIMIT 5""")

    records = sql.fetchall()
    good_attempts = 0
    start = time.time()
    for record in records:
        question, prompts, answer = record
        prompts = prompts.split(',')
        random.shuffle(prompts)
        print(f'{question}')
        for prompt in prompts:
            print(f'{prompt}')
        user_answer = input('Выберите ответ: ')
        if user_answer == answer:
            good_attempts += 1
    print(f'Угадано {good_attempts} из {len(records)}. Время потрачено: {time.time() - start}')


def difficult_quiz():
    pass


def quiz(thematic, difficult):
    if thematic:
        pass

    if difficult:
        pass


thematic_quiz()
