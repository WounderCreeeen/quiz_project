import os
from flask import *
from db_scripts import *
from random import randint, shuffle


def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0


def end_quiz():
    session.clear()


def quiz_form():
    text1 = '''<html><body><h2>Выберите викторину: <h2><form method="post" action="index"><select name="quiz">'''
    text2 = '''<p><input type="submit" value="Выбрать"></p>'''
    text3 = '''</select'''
    text4 = '''</form></body></html>'''
    options = ''' '''
    q_list = get_quizes()
    for id, name in q_list:
        text = ('''<option value="''' + str(id) + '''">''' + str(name) + '''</option>''')
        options = options + text
    return text1 + options + text3


def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        pass

    max_quiz = 3
    session['quiz'] = randint(1, max_quiz)
    session['last_question'] = 0
    return '<a href="/test">Тест</a>'


def save_answers():
    answer = request.form.get('ans_text')
    question_id = request.form.get('q_id')
    session['last_question'] = question_id
    session['total'] += 1
    if check_answer(question_id, answer):
        session['answers'] += 1


def question_form(question):
    answers_list = [
        question[2], question[3], question[4], question[5]
    ]
    shuffle(answers_list)
    return render_template('test.html', question=question[1], quest_id=question[0], answers_list=answers_list)


def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            # session['last_question'] = result[0]
            return redirect(url_for('result'))
        return question_form(next_question)


def result():
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html


folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/index', 'index', index, methods=['post', 'get'])
app.add_url_rule('/test', 'test', test, methods=['post', 'get'])
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = 'MayonnaiseOnAnEscalator'

if __name__ == '__main__':
    app.run()
