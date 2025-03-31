from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from controller.database import db
from controller.config import config
from controller.Models import *





app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(config)
app.config['SECRET_KEY'] = 'RadhaSwami@JSRS'

db.init_app(app)

with app.app_context():
    db.create_all()

    user_data = User.query.filter_by(user_email='riteshbhojgi@gmail.com').first()
    if not user_data:
        user = User( user_email='riteshbhojgi@gmail.com', user_passw='@2Admin', user_name='admin', user_qualification='Supreme', user_dob='14/05/2003', user_status='active')
        db.session.add(user)
        db.session.commit()


from controller.auth_routes import *
from controller.routes import *



if __name__ == '__main__':
    app.run(debug=True)
