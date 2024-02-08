import sqlite3
from random import randint

bd_name = 'quiz.sqlite'
conn = None
cursor = None


def open_db():
    global conn, cursor
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()


def close_db():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    open_db()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close_db()


def create_db():
    open_db()
    cursor.execute('''PRAGMA foreign_keys=on''')

    do('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY, 
            name VARCHAR)'''
       )
    do('''CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY, 
                question VARCHAR, 
                answer VARCHAR, 
                wrong1 VARCHAR, 
                wrong2 VARCHAR, 
                wrong3 VARCHAR)'''
       )
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_id INTEGER,
                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                FOREIGN KEY (question_id) REFERENCES question (id) )'''
       )
    close_db()


def show(table):
    query = 'SELECT * FROM ' + table
    open_db()
    cursor.execute(query)
    print(cursor.fetchall())
    close_db()


def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')


def add_questions():
    questions = [
        ('Какой город является столицей Франции?', 'Париж', 'Львов', 'Марсель', 'Тулу'),
        ('Какой город является столицей Германии?', 'Берлин', 'Гамбург', 'Мюнхен', 'Франкфурт'),
        ('Какой город является столицей США?', 'Вашингтон', 'Нью-Йорк', 'Чикаго', 'Лос-Анджелес'),
        ('Какой город является столицей Великобритании?', 'Лондон', 'Эдинбург', 'Бермингем', 'Кардифф'),
        ('Какой город является столицей Италии?', 'Рим', 'Наполеон', 'Милан', 'Турин'),
        ('Какой город является столицей Испании?', 'Мадрид', 'Барселона', 'Севиль', 'Валенсия'),
        ('Какой город является столицей Японии?', 'Токио', 'Осака', 'Киото', 'Нагоя')
    ]
    open_db()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''',
                       questions)
    conn.commit()
    close_db()


def add_quiz():
    quizes = [
        ('q1',),
        ('q2',),
        ('q3',)
    ]
    open_db()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close_db()


def add_links():
    open_db()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Добавить связь (y / n)?")
    while answer != 'n':
        quiz_id = int(input("id викторины: "))
        question_id = int(input("id вопроса: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Добавить связь (y / n)?")
    close_db()


def get_question_after(last_id=0, vict_id=1):
    open_db()
    query = '''
        SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
        FROM question, quiz_content 
        WHERE quiz_content.question_id == question.id
        AND quiz_content.id > ? AND quiz_content.quiz_id == ? 
        ORDER BY quiz_content.id '''
    cursor.execute(query, [last_id, vict_id])
    result = cursor.fetchone()
    close_db()
    return result


def get_quizes():
    query = 'SELECT * FROM quiz ORDER BY id'
    open_db()
    cursor.execute(query)
    result = cursor.fetchall()
    close_db()
    return result


def get_quiz_count():
    query = 'SELECT MAX(quiz_id) FROM quiz_content'
    open_db()
    cursor.execute(query)
    result = cursor.fetchone()
    close_db()
    return result


def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open_db()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids) - 1)
    rand_id = ids[rand_num][0]
    close_db()
    return rand_id


def check_answer(q_id, ans_text):
    query = '''
    SELECT question.answer
    FROM quiz_content, question
    WHERE quiz_content.id = ?
    AND quiz_content.question_id = question_id
    '''
    open_db()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close_db()
    if result is None:
        return False
    else:
        if result[0] == ans_text:
            return True
        return False


def main():
    clear_db()
    create_db()
    add_questions()
    add_quiz()
    show_tables()
    add_links()
    show_tables()
    # print(get_question_after(0, 3))
    # print(get_quiz_count())
    # print(get_random_quiz_id())


if __name__ == '__main__':
    main()
