# Здесь будет код веб-приложения
import sqlite3

bd_name = 'quiz.sqlite'
conn = None
cursor = None


def open_db():
    global conn, cursor
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()


def close_db():
    cursor.close()
    conn.commit()


def do(query):
    cursor.execute(query)
    conn.commit()

def show(table):
    query = 'SELECT * FROM ' + table
    open_db()
    cursor.execute(query)
    print(cursor.fetchall())
    close_db()

def create_db():
    open_db()
    cursor.execute('PRAGMA foreign_keys=on')
    do("""CREATE TABLE IF NOT EXISTS quiz (
            quiz_id INTAGER PRIMARY KEY, name VARCHAR)""")

    do("""CREATE TABLE IF NOT EXISTS question (
        question_id INTAGER PRIMARY KEY,
            question VARCHAR,
            answer VARCHAR,
            wrong1 VARCHAR,
            wrong2 VARCHAR,
            wrong3 VARCHAR)""")

    do("""CREATE TABLE IF NOT EXISTS quiz_content (
        id INTAGER PRIMARY KEY,
        question_id INTAGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id))""")
    close_db()


def clear_db():
    open_db()
    query = """DROP TABLE IF EXISTS quiz_content"""
    do(query)
    query = """DROP TABLE IF EXISTS question"""
    do(query)
    query = """DROP TABLE IF EXISTS quiz"""
    do(query)
    close_db()

def add_quiz():
    quizes = [
        ('Своя игра'),
        ('Кто хочет стать миллионером'),
        ('Самый умный')
    ]
    open_db()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''')

def add_questions():
    questions = [
        ('q1','ra1','wa11','wa12','wa13'),
        ('q2','ra2','wa21','wa22','wa23'),
        ('q3','ra3','wa31','wa32','wa33'),
        ('q4','ra4','wa41','wa42','wa43'),
        ('q5','ra5','wa51','wa52','wa53'),
        ('q6','ra6','wa61','wa62','wa63'),
        ('q7','ra7','wa71','wa72','wa73')
    ]
    open_db()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)''',
                       questions
    )
    conn.commit()
    close_db()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def add_links():
    open_db()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query='INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)'
    answer=input('Добавить связь (y/n)?')
    while answer != 'n':
        quiz_id = int(input('id викторины'))
        question_id = int(input('id вопроса'))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input('Добавить связь (y/n)?')
    close_db()

def get_question_after(question_id=0,quiz_id=1):
    open_db()
    query='''
    SELECT quiz_content.id, question.question, question.answer,
    question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id
    '''
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close_db()
    return result

def get_quizes():
    query = 'SELECT = FROM quiz ORDER BY id'
    open_db()
    cursor.execute(query)
    result = cursor.fetchall()
    close_db()
    return result

def main():
    clear_db()
    create_db()
    add_questions()
    add_quiz()
    add_links()
    show_tables()
    #print(get_question_after(3,1))

if __name__ == '__main__':
    main()