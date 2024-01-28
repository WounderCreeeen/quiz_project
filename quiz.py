from flask import *
from db_scripts import *
from random import randint

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    text1 = '''
    <html><body><h2>Выберите викторину: <h2><form method="post" action="index"><select name="quiz">
    '''
    text2 = '''
    <p><input type="submit" value="Выбрать"></p>
    '''
    text3='''</select'''

    text4 = '''</form></body></html>'''
def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        end_quiz()

    max_quiz = 3
    session['quiz'] = randint(1, max_quiz)
    session['last_question'] = 0
    return '<a href="/test">Тест</a>'
def test():
    result = get_question_after(session['last_question'], session['quiz'])
    if result is None or len(result) == 0:
        return redirect(url_for('result'))
    else:
        session['last_question'] = result[0]
        string = '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'
        return string
def result():
    return 'это все вопросы'


app = Flask(__name__)
app.app_url_rule('/', 'index', index)
app.app_url_rule('/', 'test', test)
app.app_url_rule('/', 'result', result)

app.config['SECRET_KEY'] = 'Mayonnaise on an escalator'

if __name__ = '__main__':
    app.run()