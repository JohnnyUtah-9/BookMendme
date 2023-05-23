from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/johnnyutah/PycharmProjects/BookMendme1/your_database.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = os.urandom(24)

# This is your model definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    books = db.Column(db.String(100), nullable=False)
    # more columns...

with app.app_context():
    db.create_all()

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        return 'User added successfully'
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
