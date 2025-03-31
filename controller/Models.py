from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):  
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)  
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_passw = db.Column(db.String(120), nullable=False)
    user_name = db.Column(db.String(120), unique=True, nullable=False)  
    user_qualification = db.Column(db.String(120), nullable=True)
    user_dob = db.Column(db.String(120), nullable=False)
    user_status = db.Column(db.String(120), nullable=False, default='active')
    user_quiz_attempts = db.relationship('QuizAttempt', back_populates='user', overlaps="quiz_attempts")
    quiz_attempts = db.relationship('QuizAttempt', overlaps="user_quiz_attempts")


class Admin(db.Model):  
    admin_id = db.Column(db.Integer, primary_key=True)  
    admin_email = db.Column(db.String(120), unique=True, nullable=False)
    admin_passw = db.Column(db.String(120), nullable=False)
    AdminName = db.Column(db.String(120),nullable=False)  

class Subject(db.Model):  
    subj_id = db.Column(db.Integer, primary_key=True)  
    subj_name = db.Column(db.String(120), unique=True, nullable=False)
    subj_descr = db.Column(db.String, nullable=False)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

class Chapter(db.Model):  
    chap_id = db.Column(db.Integer, primary_key=True, nullable=False)  
    chap_name = db.Column(db.String(120),nullable=False)
    chap_descr = db.Column(db.String, nullable=False)
    subj_id = db.Column(db.Integer, db.ForeignKey('subject.subj_id'))
    quizes = db.relationship('Quiz', backref='chapter', lazy=True)
    


class Quiz(db.Model):  
    quiz_id = db.Column(db.Integer, primary_key=True)  
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chap_id'))
    date_of_quiz = db.Column(db.Date, nullable=False)
    quiz_name = db.Column(db.String(120), unique=False, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String, nullable=True)


class Ques(db.Model):  
    ques_id = db.Column(db.Integer, primary_key=True, nullable=False)  
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    ques_statment = db.Column(db.String(120), nullable=False)
    option1 = db.Column(db.String(120), nullable=False)
    option2 = db.Column(db.String(120), nullable=False)
    option3 = db.Column(db.String(120), nullable=False)
    option4 = db.Column(db.String(120), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

    quiz = db.relationship('Quiz', backref='ques')


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    attempt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    attempt_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='user_quiz_attempts', overlaps="quiz_attempts,user_quiz_attempts")
    quiz = db.relationship('Quiz', backref='quiz_attempts', foreign_keys=[quiz_id])