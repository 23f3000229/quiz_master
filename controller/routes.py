import sqlite3
from main import app
from flask import render_template, request, redirect, url_for, session, flash
from controller.Models import * 
from datetime import datetime
from controller.Models import Ques, Quiz, Chapter, Subject, User


@app.route('/')
def home():
    if 'user_email' in session:
        return render_template('home.html',subjects=Subject.query.all(),chapters=Chapter.query.all())
    else:
        return redirect(url_for('login'))

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    if 'admin' in session.get('user_name', None):
        if request.method == 'GET':
            return render_template('add_subject.html')
        
        if request.method == 'POST':
            name=request.form.get('subject_name', None)
            description=request.form.get('subject_description', None)

            #data validation
            subject=Subject.query.filter_by(subj_name=name).first()
            if subject:
                flash('Subject already exists !')
                return render_template('add_subject.html')
            if not name or not description:
                flash('Subject name is required !')
                return render_template('add_subject.html')
            
            new_subject=Subject(subj_name=name, subj_descr=description)
            db.session.add(new_subject)
            db.session.commit()
            flash('Subject added successfully !')
            return redirect(url_for('home'))


    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))


@app.route('/add_chapter', methods=['GET', 'POST'])
def add_chapter(): 
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        subjects = Subject.query.all()
        return render_template('add_chapter.html', all_subjects=subjects)
    
    if request.method == 'POST':
        name = request.form.get('chap_name', None)
        description = request.form.get('chap_description', None)
        subject_id = request.form.get('subj_id', None)
        
      
        # Data validation

        
        if not name or not description or not subject_id:
            flash('All fields are required!')
            subjects = Subject.query.all()
            return render_template('add_chapter.html', all_subjects=subjects)

        chapter = Chapter.query.filter_by(chap_name=name, subj_id=subject_id).first()
        if chapter:
            flash('Chapter already exists!')
            subjects = Subject.query.all()
            return render_template('add_chapter.html', all_subjects=subjects)

        new_chapter = Chapter(chap_name=name, chap_descr=description, subj_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        flash('Chapter added successfully!')
        return redirect(url_for('home'))   

@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        chapters = Chapter.query.all()
        return render_template('add_quiz.html', all_chapters=chapters)
    
    if request.method == 'POST':
        chapter_id = request.form.get('chapter_id', None)
        quiz_name = request.form.get('quiz_name', None)
        date_str = request.form.get('date_of_quiz', None)
        time_duration = request.form.get('time_duration', None)
        remarks = request.form.get('remarks', None)

        # Convert date string to date object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format!')
            chapters = Chapter.query.all()
            return render_template('add_quiz.html', all_chapters=chapters)

        # Data validation
        if not chapter_id or not quiz_name or not date or not time_duration or not remarks:
            flash('All fields are required!')
            chapters = Chapter.query.all()
            return render_template('add_quiz.html', all_chapters=chapters)

        quiz = Quiz.query.filter_by(quiz_name=quiz_name, chapter_id=chapter_id).first()
        if quiz:
            flash('Quiz already exists!')
            chapters = Chapter.query.all()
            return render_template('add_quiz.html', all_chapters=chapters)

        new_quiz = Quiz(chapter_id=chapter_id, quiz_name=quiz_name , date_of_quiz=date, time_duration=time_duration, remarks=remarks)
        db.session.add(new_quiz)
        db.session.commit()
        flash('Quiz added successfully!')
        return redirect(url_for('home'))

@app.route('/add_quizto_chap <int:chapter_id>', methods=['GET', 'POST'])
def add_quizto_chap(chapter_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzes'))
    
    if request.method == 'GET':
        return render_template('add_quizto_chap.html', chapter_id=chapter_id )
    
    if request.method == 'POST':
        quiz_name = request.form.get('quiz_name', None)
        chapter_id = chapter_id
        date_str = request.form.get('date_of_quiz', None)
        time_duration = request.form.get('time_duration', None)
        remarks = request.form.get('remarks', None)

        # Convert date string to date object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format!')
            return render_template('add_quizto_chap.html', chapter_id=chapter_id)

        # Data validation
        if not chapter_id or not quiz_name or not date or not time_duration or not remarks:
            flash('All fields are required!')
            return render_template('add_quizto_chap.html', chapter_id=chapter_id)

        quiz = Quiz.query.filter_by(quiz_name=quiz_name, chapter_id=chapter_id).first()
        if quiz:
            flash('Quiz already exists!')
            return render_template('add_quizto_chap.html', chapter_id=chapter_id)

        new_quiz = Quiz(quiz_name=quiz_name, chapter_id=chapter_id, date_of_quiz=date, time_duration=time_duration, remarks=remarks)
        db.session.add(new_quiz)
        db.session.commit()
        flash('Quiz added successfully!')
        return redirect(url_for('quizzes', chapter_id=chapter_id))

@app.route('/add_question <int:quiz_id> ', methods=['GET', 'POST'])
def add_question(quiz_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        quizzes = Quiz.query.all()
        return render_template('add_question.html', quiz_id=quiz_id)
    
    if request.method == 'POST':
        quiz_id = quiz_id
        ques_statment = request.form.get('ques_statment', None)
        option1 = request.form.get('option1', None)
        option2 = request.form.get('option2', None)
        option3 = request.form.get('option3', None)
        option4 = request.form.get('option4', None)
        correct_option = request.form.get('correct_option', None)

        # Debugging statements
        print(f"quiz_id: {quiz_id}")
        print(f"ques_statment: {ques_statment}")
        print(f"option1: {option1}")
        print(f"option2: {option2}")
        print(f"option3: {option3}")
        print(f"option4: {option4}")
        print(f"correct_option: {correct_option}")

        # Data validation
        if not quiz_id or not option1 or not option2 or not option3 or not option4 or not correct_option:
            flash('All fields are required!')
            quizzes = Quiz.query.all()
            return render_template('add_question.html', all_quizzes=quizzes)

        new_question = Ques(quiz_id=quiz_id, ques_statment=ques_statment, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option)
        db.session.add(new_question)
        db.session.commit()
        flash('Question added successfully!')
        return redirect(url_for('questions',quiz_id=quiz_id))
    
@app.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist!')
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('edit_subject.html', subject=subject)
    
    if request.method == 'POST':
        name = request.form.get('subject_name', None)
        description = request.form.get('subject_description', None)

        # Data validation
        if not name and not description:
            flash('No changes made!')
            return render_template('edit_subject.html', subject_id=subject)
        
        subject.subj_name = name
        subject.subj_descr = description
        db.session.commit()
        flash('Subject updated successfully!')
        return redirect(url_for('manage_quiz'))

@app.route('/edit_chapter/<int:chapter_id>', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist!')
        return redirect(url_for('home'))

    if request.method == 'GET':
        subjects = Subject.query.all()
        return render_template('edit_chapter.html', chapter=chapter, all_subjects=subjects)
    
    if request.method == 'POST':
        name = request.form.get('chap_name', None)
        description = request.form.get('chap_description', None)
        subject_id = request.form.get('subj_id', None)

        # Data validation
        if not name or not description or not subject_id:
            flash('All fields are required!')
            subjects = Subject.query.all()
            return render_template('edit_chapter.html', chapter=chapter, all_subjects=subjects)

        chapter.chap_name = name
        chapter.chap_descr = description
        chapter.subj_id = subject_id
        db.session.commit()
        flash('Chapter updated successfully!')
        return redirect(url_for('manage_quiz'))

@app.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz does not exist!')
        return redirect(url_for('home'))

    if request.method == 'GET':
        chapters = Chapter.query.all()
        return render_template('edit_quiz.html', quiz=quiz, all_chapters=chapters)
    
    if request.method == 'POST':
        chapter_id = request.form.get('chapter_id', None)
        quiz_name = request.form.get('quiz_name', None)
        date_of_quiz = request.form.get('date_of_quiz', None)
        remarks = request.form.get('remarks', None)
        time_duration = request.form.get('time_duration', None)

        # Data validation
        if not chapter_id or not quiz_name or not date_of_quiz or not remarks or not time_duration:
            flash('All fields are required!')
            chapters = Chapter.query.all()
            return render_template('edit_quiz.html', quiz=quiz, all_chapters=chapters)

        # Convert date string to date object
        try:
            date_of_quiz = datetime.strptime(date_of_quiz, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format!')
            chapters = Chapter.query.all()
            return render_template('edit_quiz.html', quiz=quiz, all_chapters=chapters)

        # Update quiz details
        quiz.chapter_id = chapter_id
        quiz.quiz_name = quiz_name
        quiz.date_of_quiz = date_of_quiz
        quiz.remarks = remarks
        quiz.time_duration = time_duration

        db.session.commit()
        flash('Quiz updated successfully!')
        return redirect(url_for('home'))

@app.route('/edit_question/<int:ques_id>', methods=['GET', 'POST'])
def edit_question(ques_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to perform this action')
        return redirect(url_for('home'))
    
    # Fetch the question using the Ques model
    ques = Ques.query.get(ques_id)
    if not ques:
        flash('Question does not exist!')
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('edit_question.html', ques=ques)

    if request.method == 'POST':
        # Update question details
        ques.ques_statment = request.form.get('ques_statment')
        ques.option1 = request.form.get('option1')
        ques.option2 = request.form.get('option2')
        ques.option3 = request.form.get('option3')
        ques.option4 = request.form.get('option4')
        ques.correct_option = request.form.get('correct_option')

        db.session.commit()
        flash('Question updated successfully!')
        return redirect(url_for('questions', quiz_id=ques.quiz_id))

@app.route('/delete_subject/<int:subject_id>')
def delete_subject(subject_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    chapters= Chapter.query.filter_by(subj_id=subject_id).all()
    for chapter in chapters:
        quizzes = Quiz.query.filter_by(chapter_id=chapter.chap_id).all()
        for quiz in quizzes:
            questions = Ques.query.filter_by(quiz_id=quiz.quiz_id).all()
            for question in questions:
                db.session.delete(question)
            db.session.delete(quiz)
        db.session.delete(chapter)


    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!')
    return redirect(url_for('manage_quiz'))

@app.route('/delete_chapter/<int:chapter_id>')
def delete_chapter(chapter_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('manage_quiz'))
    
    chapters= Chapter.query.filter_by(chap_id=chapter_id).all()
    for chapter in chapters:
        quizzes = Quiz.query.filter_by(chapter_id=chapter.chap_id).all()
        for quiz in quizzes:
            questions = Ques.query.filter_by(quiz_id=quiz.quiz_id).all()
            for question in questions:
                db.session.delete(question)
            db.session.delete(quiz)
        db.session.delete(chapter)
        db.session.commit()
        flash('Chapter deleted successfully!')
        return redirect(url_for('manage_quiz'))

@app.route('/delete_quiz/<int:quiz_id>')
def delete_quiz(quiz_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz does not exist!')
        return redirect(url_for('manage_quiz'))

    # Delete all questions associated with the quiz
    questions = Ques.query.filter_by(quiz_id=Quiz.quiz_id).all()
    for question in questions:
        db.session.delete(question)

    # Delete the quiz
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!')
    return redirect(url_for('quizzes', chapter_id=quiz.chapter_id))

@app.route('/quizzes/<int:chapter_id>')
def quizzes(chapter_id):
    if 'user_email' not in session:
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))

    # Fetch the chapter details
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter not found!')
        return redirect(url_for('home'))

    #setting session for chapter
    session['chap_name'] = chapter.chap_name

    # Fetch all quizzes for the chapter
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()

    
    
    return render_template('quizzes.html', quizzes=quizzes, chapter=chapter)

@app.route('/questions/<int:quiz_id>', methods=['GET'])
def questions(quiz_id):
    if 'user_email' not in session:
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))

    # Fetch the quiz details
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz not found!')
        return redirect(url_for('home'))

    # Fetch all questions for the quiz
    questions = Ques.query.filter_by(quiz_id=quiz_id).all()

    return render_template('questions.html', quiz=quiz, questions=questions)

@app.route('/submit_answers/<int:quiz_id>', methods=['POST'])
def submit_answers(quiz_id):
    if 'user_email' not in session:
        flash('You are not authorized to perform this action')
        return redirect(url_for('home'))

    # Fetch the quiz details
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz not found!')
        return redirect(url_for('home'))

    # Process the submitted answers
    submitted_answers = {}
    for question in quiz.questions:  # Assuming `quiz.questions` gives all questions for the quiz
        answer = request.form.get(f'answer_{question.ques_id}')
        submitted_answers[question.ques_id] = answer

    # Example: Check answers and calculate score
    score = 0
    for question_id, answer in submitted_answers.items():
        question = Ques.query.get(question_id)
        if question and question.correct_option == answer:
            score += 1

    flash(f'You scored {score}/{len(quiz.questions)}!')
    return redirect(url_for('questions', quiz_id=quiz_id))




@app.route('/delete_question/<int:question_id>', methods=['GET'])
def delete_question(question_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to perform this action')
        return redirect(url_for('home'))

    question = Ques.query.get(question_id)
    if not question:
        flash('Question not found!')
        return redirect(url_for('home'))

    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!')
    return redirect(url_for('questions', quiz_id=quiz_id))
   
@app.route('/user_dashboard')
def user_d():
    return render_template('user_dashboard.html')

@app.route('/admin_dashboard')
def admin_d():
    subjects = Subject.query.all()
    return render_template('admin_dashboard.html', subjects=subjects)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Check if already logged in
        if 'user_email' in session:
            flash('You are already logged in !')
            return redirect('/')
        return render_template('register.html')

    if request.method == 'POST':
        # Get form data
        name = request.form.get('user_name', None)
        email = request.form.get('user_email', None)
        password = request.form.get('user_passw', None)
        confirm_password = request.form.get('confirm_password', None)
        dob = request.form.get('user_dob', None)
        qualification = request.form.get('qualification', None)


        # Data validation
        if not name or not email or not password or not confirm_password or not dob or not qualification:
            flash('All fields are required !')
            return render_template('register.html')

        if '@' not in email:
            flash('Invalid Email !')
            return render_template('register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters long !')
            return render_template('register.html')
        
        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one digit !')
            return render_template('register.html')
        
        if not any(char.isalpha() for char in password):
            flash('Password must contain at least one letter !')
            return render_template('register.html')
        
        if not any(char in '!@#$%^&*()_+' for char in password):
            flash('Password must contain at least one special character !')
            return render_template('register.html')

        

        if password != confirm_password:
            flash('Passwords do not match !')
            return render_template('register.html')
    
        # Check if user already exists
        existing_user = User.query.filter_by(user_email=email).first()  
        if existing_user:
            flash('User already exists !')
            return render_template('register.html')

        # Create new user
        new_user = User(user_name=name, user_email=email, user_passw=password, user_dob=dob, user_qualification=qualification)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful !')
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        #check if already logged in
        if 'user_email' in session:
            flash('You are already logged in !')
            return redirect('/')
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)

        #data validation
        if not email:
            flash('Email is required !')
            return render_template('login.html')

        if '@' not in email: 
            flash('Invalid Email !')
            return render_template('login.html')
        
        #add more data validations here

        #check if user exists

        user = User.query.filter_by(user_email=email).first()
        if not user:
            flash('User does not exist !')
            return render_template('login.html')
        
        #check password
        if user.user_passw != password:
            flash('Invalid Password !')
            return render_template('login.html')
        
        if user.user_status == 'inactive':
            flash('Your account is inactive !')
            return render_template('login.html')
        
        #login user / create session

        session['user_email'] = user.user_email
        session['user_name'] = user.user_name
        

        flash('Login Successfull !')
        return redirect(url_for('home'))

 
@app.route('/logout')
def logout():
    #check if user is logged in
    if 'user_email' not in session:
        flash('You are not logged in !')
        return redirect('login')
    
    session.pop('user_email',None)
    session.pop('user_name',None)
    flash('Logged out successfully !')
    return redirect(url_for('login'))

@app.route('/manage_quiz')
def manage_quiz():
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))

    subjects = Subject.query.all()
    return render_template('manage_quiz.html', subjects=subjects)

@app.route('/explore_quizzes')
def explore_quizzes ():
    if 'user_email' not in session:
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))

    subjects = Subject.query.all()
    return render_template('explore_quizzes.html', subjects=subjects)

@app.route('/manage_users')
def manage_users():
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page')
        return redirect(url_for('home'))
    
    try:
        import os
        conn = sqlite3.connect(os.path.join('instance', 'database.sqlite3'))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        flash('Database error occurred!')
        return redirect(url_for('home'))

    # Convert the list of tuples to a list of dictionaries for easier rendering in templates
    user_list = []
    for user in users:
        user_dict = {
            'user_id': user[0],
            'user_email': user[1],
            'user_pass': user[2],
            'user_name': user[3],
            'user_qualification': user[4],
            'user_dob': user[5],
            'user_status': user[6]  # Ensure user_status is included
        }
        user_list.append(user_dict)

    return render_template('manage_users.html', users=user_list)


@app.route('/toggle_user_status/<int:user_id>')
def toggle_user_status(user_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to perform this action')
        return redirect(url_for('home'))

    user = User.query.get(user_id)
    if not user:
        flash('User does not exist!')
        return redirect(url_for('manage_users'))

    # Toggle user status
    if user.user_status == 'active':
        user.user_status = 'inactive'
    else:
        user.user_status = 'active'

    db.session.commit()

    flash(f"User status updated to {'Blocked' if user.user_status == 'inactive' else 'Active'}!")
    return redirect(url_for('manage_users'))


@app.route('/view_user_scores/<int:user_id>')
def view_user_scores(user_id):
    # Mock data for user scores
    user_scores = {
        1: {"quizzes_taken": 5, "average_score": 85},
        2: {"quizzes_taken": 3, "average_score": 70},
        3: {"quizzes_taken": 7, "average_score": 90},
    }
    scores = user_scores.get(user_id, {})
    return render_template('user_scores.html', user_id=user_id, scores=scores)

@app.route('/view_user_scores_individually/<int:user_id>')
def view_user_scores_individually(user_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page!')
        return redirect(url_for('home'))

    # Fetch the user details
    user = User.query.get(user_id)
    if not user:
        flash('User not found!')
        return redirect(url_for('manage_users'))

    # Fetch all quiz attempts for the user
    attempts = QuizAttempt.query.filter_by(user_id=user_id).join(Quiz, QuizAttempt.quiz_id == Quiz.quiz_id) \
                                .add_columns(
                                    Quiz.quiz_name,
                                    QuizAttempt.score,
                                    QuizAttempt.total_score,
                                    QuizAttempt.attempt_date
                                ).all()

    return render_template('view_user_scores.html', user=user, attempts=attempts)

@app.route('/admin_scores')
def admin_scores():
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page!')
        return redirect(url_for('home'))

    # Fetch all quiz attempts with user and quiz details
    attempts = QuizAttempt.query.join(User, QuizAttempt.user_id == User.user_id) \
                                .join(Quiz, QuizAttempt.quiz_id == Quiz.quiz_id) \
                                .add_columns(
                                    User.user_name.label('user_name'),
                                    Quiz.quiz_name.label('quiz_name'),
                                    QuizAttempt.score,
                                    QuizAttempt.total_score,
                                    QuizAttempt.attempt_date
                                ).all()

    return render_template('admin_scores.html', attempts=attempts)

@app.route('/user_scores')
def user_scores():
    if 'user_email' not in session:
        flash('You need to log in to view your scores!')
        return redirect(url_for('login'))

    user = User.query.filter_by(user_email=session['user_email']).first()
    attempts = QuizAttempt.query.filter_by(user_id=user.user_id).all()
    return render_template('user_scores.html', attempts=attempts)

@app.route('/attempt_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def attempt_quiz(quiz_id):
    if 'user_email' not in session:
        flash('You need to log in to attempt quizzes!')
        return redirect(url_for('login'))

    # Fetch the quiz details
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz not found!')
        return redirect(url_for('home'))

    # Check if the quiz deadline has passed
    current_date = datetime.now().date()
    if current_date > quiz.date_of_quiz:
        flash('The deadline to attempt this quiz has passed!')
        return redirect(url_for('home'))

    if request.method == 'GET':
        # Use quiz.ques to access the questions
        questions = quiz.ques
        return render_template('attempt_quiz.html', quiz=quiz, questions=questions)

    if request.method == 'POST':
        # Process submitted answers
        feedback = []
        score = 0
        total_score = 0

        for question in quiz.ques:
            total_score += 1  # Assuming each question has a score of 1
            submitted_answer = request.form.get(f'answer_{question.ques_id}')
            correct = False
            if submitted_answer and int(submitted_answer) == question.correct_option:
                score += 1
                correct = True

            # Add feedback for each question
            feedback.append({
                'question': question.ques_statment,
                'submitted_answer': submitted_answer,
                'correct_answer': question.correct_option,
                'is_correct': correct
            })

        # Save the quiz attempt
        user = User.query.filter_by(user_email=session['user_email']).first()
        quiz_attempt = QuizAttempt(
            user_id=user.user_id,
            quiz_id=quiz_id,
            score=score,
            total_score=total_score
        )
        db.session.add(quiz_attempt)
        db.session.commit()

        # Redirect to the results page with feedback
        return render_template('quiz_results.html', quiz=quiz, feedback=feedback, score=score, total_score=total_score)

@app.route('/view_chapter_scores/<int:chapter_id>')
def view_chapter_scores(chapter_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page!')
        return redirect(url_for('home'))

    # Fetch the chapter details
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter not found!')
        return redirect(url_for('manage_quiz'))

    # Fetch all quizzes in the chapter
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    quiz_ids = [quiz.quiz_id for quiz in quizzes]

    # Fetch all quiz attempts for quizzes in the chapter
    attempts = QuizAttempt.query.filter(QuizAttempt.quiz_id.in_(quiz_ids)) \
                                .join(User, QuizAttempt.user_id == User.user_id) \
                                .join(Quiz, QuizAttempt.quiz_id == Quiz.quiz_id) \
                                .add_columns(
                                    User.user_name,
                                    Quiz.quiz_name,
                                    QuizAttempt.score,
                                    QuizAttempt.total_score,
                                    QuizAttempt.attempt_date
                                ).all()

    return render_template('view_chapter_scores.html', chapter=chapter, attempts=attempts)

@app.route('/view_quiz_scores/<int:quiz_id>')
def view_quiz_scores(quiz_id):
    if 'admin' not in session.get('user_name', None):
        flash('You are not authorized to view this page!')
        return redirect(url_for('home'))

    # Fetch the quiz details
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz not found!')
        return redirect(url_for('quizzes'))

    # Fetch all quiz attempts for the specific quiz
    attempts = QuizAttempt.query.filter_by(quiz_id=quiz_id).join(User, QuizAttempt.user_id == User.user_id) \
                                .add_columns(
                                    User.user_name,
                                    QuizAttempt.score,
                                    QuizAttempt.total_score,
                                    QuizAttempt.attempt_date
                                ).all()

    return render_template('view_quiz_scores.html', quiz=quiz, attempts=attempts)

@app.route('/view_chapters/<int:subject_id>')
def view_chapters(subject_id):
    if 'user_email' not in session:
        flash('You need to log in to view chapters!')
        return redirect(url_for('login'))

    # Fetch the subject details
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found!')
        return redirect(url_for('home'))

    # Fetch chapters for the subject
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()

    return render_template('view_chapters.html', subject=subject, chapters=chapters)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        flash('Please enter a search term.')
        return redirect(url_for('home'))

    # Search for subjects, chapters, and quizzes
    subjects = Subject.query.filter(Subject.subj_name.ilike(f"%{query}%")).all()
    chapters = Chapter.query.filter(Chapter.chap_name.ilike(f"%{query}%")).all()
    quizzes = Quiz.query.filter(Quiz.quiz_name.ilike(f"%{query}%")).all()

    # Check if the user is an admin before searching for users
    users = []
    if 'admin' in session.get('user_name', '').lower():
        users = User.query.filter(
            (User.user_name.ilike(f"%{query}%")) | (User.user_email.ilike(f"%{query}%"))
        ).all()

    return render_template(
        'search_results.html',
        query=query,
        subjects=subjects,
        chapters=chapters,
        quizzes=quizzes,
        users=users
    )
@app.route('/subject/<int:subject_id>')
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subj_id=subject_id).all()
    return render_template('view_item.html', context='subject', subject=subject, chapters=chapters)

@app.route('/chapter/<int:chapter_id>')
def view_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return render_template('view_item.html', context='chapter', chapter=chapter, quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>')
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('view_item.html', context='quiz', quiz=quiz)


@app.route('/admin_summary')
def admin_summary():
    if 'admin' not in session.get('user_name', '').lower():
        flash('You are not authorized to view this page!')
        return redirect(url_for('home'))

    # Basic statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(user_status='active').count()
    inactive_users = User.query.filter_by(user_status='inactive').count()
    total_quizzes = Quiz.query.count()
    avg_quiz_score = db.session.query(db.func.avg(QuizAttempt.score)).scalar()

    # Additional insights
    total_quiz_attempts = QuizAttempt.query.count()
    top_quiz = (
        db.session.query(Quiz.quiz_name, Chapter.chap_name, db.func.avg(QuizAttempt.score).label('avg_score'))
        .join(QuizAttempt, Quiz.quiz_id == QuizAttempt.quiz_id)
        .join(Chapter, Quiz.chapter_id == Chapter.chap_id)
        .group_by(Quiz.quiz_id, Chapter.chap_name)
        .order_by(db.desc('avg_score'))
        .first()
    )
    most_active_user = (
        db.session.query(User.user_name, db.func.count(QuizAttempt.attempt_id).label('attempt_count'))
        .join(QuizAttempt, User.user_id == QuizAttempt.user_id)
        .group_by(User.user_id)
        .order_by(db.desc('attempt_count'))
        .first()
    )
    inactive_users_percentage = (inactive_users / total_users * 100) if total_users > 0 else 0
    avg_quizzes_per_user = (total_quiz_attempts / total_users) if total_users > 0 else 0

    return render_template(
        'admin_summary.html',
        total_users=total_users,
        active_users=active_users,
        inactive_users=inactive_users,
        total_quizzes=total_quizzes,
        avg_quiz_score=round(avg_quiz_score, 2) if avg_quiz_score else 0,
        total_quiz_attempts=total_quiz_attempts,
        top_quiz=top_quiz,
        most_active_user=most_active_user,
        inactive_users_percentage=round(inactive_users_percentage, 2),
        avg_quizzes_per_user=round(avg_quizzes_per_user, 2)
    )

@app.route('/user_summary')
def user_summary():
    if 'user_email' not in session:
        flash('You need to log in to view your progress!')
        return redirect(url_for('login'))

    # Fetch the logged-in user
    user = User.query.filter_by(user_email=session['user_email']).first()

    # Fetch all quiz attempts for the user
    attempts = QuizAttempt.query.filter_by(user_id=user.user_id).join(Quiz, QuizAttempt.quiz_id == Quiz.quiz_id) \
                                .add_columns(
                                    Quiz.quiz_name,
                                    QuizAttempt.score,
                                    QuizAttempt.total_score,
                                    QuizAttempt.attempt_date
                                ).all()

    # Calculate user's insights
    total_quizzes_attempted = len(attempts)
    total_score = sum(attempt.score for attempt in attempts)
    total_possible_score = sum(attempt.total_score for attempt in attempts)
    average_score = (total_score / total_possible_score * 100) if total_possible_score > 0 else 0

    best_quiz = max(attempts, key=lambda x: x.score / x.total_score if x.total_score > 0 else 0, default=None)
    worst_quiz = min(attempts, key=lambda x: x.score / x.total_score if x.total_score > 0 else 0, default=None)

    # Comparison metrics
    all_users = (
        db.session.query(User.user_name, db.func.avg(QuizAttempt.score / QuizAttempt.total_score * 100).label('avg_score'))
        .join(QuizAttempt, User.user_id == QuizAttempt.user_id)
        .group_by(User.user_id)
        .all()
    )
    all_users_sorted = sorted(all_users, key=lambda x: x.avg_score if x.avg_score else 0, reverse=True)
    user_rank = next((index + 1 for index, u in enumerate(all_users_sorted) if u.user_name == user.user_name), None)
    overall_avg_score = sum(u.avg_score for u in all_users if u.avg_score) / len(all_users) if all_users else 0
    top_user = max(all_users, key=lambda x: x.avg_score if x.avg_score else 0, default=None)
    lowest_user = min(all_users, key=lambda x: x.avg_score if x.avg_score else 0, default=None)

    return render_template(
        'user_summary.html',
        user=user,
        total_quizzes_attempted=total_quizzes_attempted,
        average_score=round(average_score, 2),
        best_quiz=best_quiz,
        worst_quiz=worst_quiz,
        attempts=attempts,
        user_rank=user_rank,
        overall_avg_score=round(overall_avg_score, 2),
        top_user=top_user,
        lowest_user=lowest_user
    )




