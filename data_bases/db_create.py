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
                       + """ (question text, prompts text, answer text, 
                       UNIQUE (question, prompts, answer))""")

        with open(f'thematic/{name}.txt', 'r', encoding='utf-8') as f:
            data = f.readline()
            while data:
                ins_data = tuple(i.strip() for i in data.split(';'))
                cursor.execute(f"""INSERT OR IGNORE INTO {name} VALUES {ins_data}""")
                data = f.readline()

        db.commit()


def create_difficult_db():
    names = get_file_names('difficult')

    db = sqlite3.connect('difficult_quiz.db')
    cursor = db.cursor()

    for name in names:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}"""
                       + """ (question text, answer text, UNIQUE (question, answer))""")

        with open(f'difficult/{name}.txt', 'r', encoding='utf-8') as f:
            data = f.readline()
            while data:
                ins_data = tuple(i.strip() for i in data.split('*'))
                cursor.execute(f"""INSERT OR IGNORE INTO {name} VALUES {ins_data}""")
                data = f.readline()

        db.commit()


if __name__ == '__main__':
    create_thematic_db()
    create_difficult_db()
