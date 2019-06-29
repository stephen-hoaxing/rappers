from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a031a8c969597bafec84182fbd1ca309'
app.config['SQLAALCHEMY_DATABASE_UTI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return self.username + ", " + self.id + ", " + self.email

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return self.title + ", " + self.id + ", " + self.date_posted + ", " + self.content

posts = [
    {
        'author': 'Nidal Chalhoub',
        'title': 'Blog Post1',
        'content': 'Content 1',
        'date_posted': '2019.06.29'
    },
    {
        'author': 'Nidal Chalhoub',
        'title': 'Blog Post2',
        'content': 'Content 2',
        'date_posted': '2019.06.29'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts, title='Normal')

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(message='Account created', category='success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title='Register')

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'admin':
            flash(message='You have been logged in', category='success')
            return redirect(url_for('home'))
        else:
            flash(message='Try again')
    return render_template('login.html', form=form, title='Login')

if __name__ == '__main__':
    app.run(debug=True)