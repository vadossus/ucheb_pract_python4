from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    login = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)

    @staticmethod
    def check_credentials(login, password):
        return Register.query.filter_by(login=login, password=password).first()
    
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(25), db.ForeignKey('register.login'), nullable=False)

def save_answer(login, score, total_questions):
    answer_text = f"{score} из {total_questions}"
    new_answer = Answer(answer=answer_text, login=login)
    db.session.add(new_answer)
    db.session.commit()
