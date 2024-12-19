from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Register, save_answer
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/quiz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '123222'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('authorisation'))

    with open('questions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)
    questions_json = json.dumps(questions, ensure_ascii=False)
    total_questions = len(questions)
    return render_template('razmetka.html', questions_json=questions_json, total_questions=total_questions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        login = request.form['login']
        password = request.form['password']
        email = request.form['email']

        new_user = Register(name=name, login=login, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('authorisation'))
    return render_template('register.html')

@app.route('/authorisation', methods=['GET', 'POST'])
def authorisation():
    session['logged_in'] = False
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = Register.check_credentials(login, password)
        if user:
            session['logged_in'] = True
            session['user_login'] = login  
            flash('Успешный вход!', 'success')
            return redirect(url_for('quiz'))
        else:
            flash('Неверные учетные данные', 'danger')

    return render_template('authorisation.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('authorisation'))

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    question_index = data['question_index']
    selected_option = data['selected_option']

    with open('questions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)

    if questions[question_index]['answer'] == selected_option:
        return jsonify({'correct': True})
    else:
        return jsonify({'correct': False})

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        score = request.form['score']
        total_questions = request.form['total_questions']
        user_login = session.get('user_login')  

        if user_login:
            save_answer(user_login, score, total_questions)  
            flash('Ответы успешно сохранены!', 'success')

    score = request.args.get('score', request.form.get('score'))
    total_questions = request.args.get('total_questions', request.form.get('total_questions'))
    return render_template('result.html', score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(debug=True)









