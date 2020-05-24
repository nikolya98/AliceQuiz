import sqlite3
import random
from db_create import create_thematic_db, create_difficult_db


def get_themes(mode=None):
    if mode == 'thematic':
        path = 'data_bases/thematic_quiz.db'
        create_thematic_db()
    if mode == 'difficult':
        path = 'data_bases/difficult_quiz.db'
        create_difficult_db()

    db = sqlite3.connect(path)
    sql = db.cursor()

    sql.execute(f"""SELECT name FROM sqlite_master WHERE type = 'table'""")
    tables_name = sql.fetchall()
    themes = []
    for name in tables_name:
        for elem in name:
            themes.append(elem)

    return themes


def thematic_quiz(user_choice):
    db = sqlite3.connect('data_bases/thematic_quiz.db')
    sql = db.cursor()

    sql.execute(f"""SELECT * FROM {user_choice} ORDER BY RANDOM() LIMIT 5""")
    records = sql.fetchall()

    for record in records:
        question, prompts, answer = record
        prompts = prompts.split(',')
        random.shuffle(prompts)
        yield question, prompts, answer

    db.close()


def difficult_quiz():
    db = sqlite3.connect('data_bases/difficult_quiz.db')
    sql = db.cursor()
    themes = get_themes('difficult')
    curr_theme = random.choice(themes)

    sql.execute(f"""SELECT * FROM {curr_theme} ORDER BY RANDOM() LIMIT 15""")
    records = sql.fetchall()

    for record in records:
        question, answer = record
        question, answer = question.replace('\\xa0', ' '), answer.replace('\\xa0', ' ') # Исправить проблему с неразрывными пробелами
        yield question, answer

    db.close()