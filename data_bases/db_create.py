import os
import sqlite3


def get_file_names(folder_name):
    # Ищем txt файлы и возвращаем их имена для дальнейшев работы с БД
    files = os.listdir(folder_name)
    file_names = [file.replace('.txt', '') for file in files if file.endswith('.txt')]
    return file_names


def create_thematic_db():
    # Создаём БД для тематических викторин
    # В качестве названия таблиц используем иена файлов с вопросами .txt
    names = get_file_names('thematic')

    db = sqlite3.connect('thematic_quiz.db')
    cursor = db.cursor()

    for name in names:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}"""
                       + """ (question text, prompts text, answer text)""")

        with open(f'thematic/{name}.txt', 'r', encoding='utf-8') as f:
            data = f.readline()
            while data:
                question, prompts, answer = data.split(';')
                cursor.execute(f"""INSERT INTO {name} VALUES """ +
                               f"""({question}, {prompts}, {answer})""")
                data = f.readline()


def create_difficult_db():
    names = get_file_names('difficult')

    db = sqlite3.connect('difficult_quiz.db')
    cursor = db.cursor()

    for name in names:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}"""
                       + """ (question text, answer text)""")

        with open(f'difficult/{name}.txt', 'r', encoding='utf-8') as f:
            data = f.readline()
            while data:
                question, answer = data.split('*')
                cursor.execute(f"""INSERT INTO {name} VALUES """ +
                               f"""({question}, {answer})""")
                data = f.readline()


