from flask import Flask, render_template, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import requests
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'POP'


@app.route('/',  methods=['POST', 'GET'])
def index():
    # x = db.execute('SELECT * FROM test').fetchall()
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        if request.form.get('password') == request.form.get('confirm_password'):
            try:
                db.execute('INSERT INTO users (username, password) VALUES (:username, :password)', {'username': request.form.get('username'), 'password': bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')})
            except:
                flash('Username is already taken', 'danger')
                return render_template('registration.html', title='Register')
            flash(f'{request.form.get("username")} successfully registered', 'success')
            db.commit()
            return render_template('index.html')
        flash('Please make sure the passwords match', 'danger')
    return render_template('registration.html', title='Register')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        t = db.execute(f'SELECT * FROM users WHERE username = :username', {'username': request.form.get('username')}).fetchone()
        if t:
            print(bcrypt.check_password_hash(t['password'], request.form.get('password')))
            if bcrypt.check_password_hash(t['password'], request.form.get('password')):
                flash(f'Welcome {request.form.get("username")}', 'success')
                return render_template('index.html')
            else:
                flash('Username or password is incorrect', 'danger')
        else:
            flash(f'No username named {request.form.get("username")} exists', 'danger')
    return render_template('login.html', title='Login')


@app.route('/<int:isbn>', methods=['POST', 'GET'])
def book(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "FqiaInArQrrxtHZ4djffQ", "isbns": isbn})
    data = dict(res.json())
    data = data['books']
    return render_template('book.html', dic = data)


@app.route('/api', methods=['POST', 'GET'])
def api():
    res = requests.get(" https://www.goodreads.com/book/isbn_to_id",
                       params={"key": "FqiaInArQrrxtHZ4djffQ", "isbn": "1632168146"})
    print(res.json())
    return f' {res.json()}'