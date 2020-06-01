from flask import Flask, render_template, request, flash, session, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import requests
from flask_bcrypt import Bcrypt
from flask_session import Session


bcrypt = Bcrypt()
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'POP'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def index():
    # x = db.execute('SELECT * FROM test').fetchall()
    if session.get('username') == None:
        session['username'] = None
    return render_template('index.html', username=session['username'])


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
            session['username'] = request.form.get('username')
            return render_template('index.html', username=session['username'])
        flash('Please make sure the passwords match', 'danger')
    return render_template('registration.html', title='Register')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['username'] = None
    flash('Successfully logged out', 'success')
    return render_template('index.html', username=session['username'])


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        t = db.execute(f'SELECT * FROM users WHERE username = :username', {'username': request.form.get('username')}).fetchone()
        if t:
            print(bcrypt.check_password_hash(t['password'], request.form.get('password')))
            if bcrypt.check_password_hash(t['password'], request.form.get('password')):
                flash(f'Welcome {request.form.get("username")}', 'success')
                session['username'] = request.form.get('username')
                return render_template('index.html', username=session['username'])
            else:
                flash('Username or password is incorrect', 'danger')
        else:
            flash(f'No username named {request.form.get("username")} exists', 'danger')
    return render_template('login.html', title='Login')


@app.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':
        isbn = db.execute("SELECT * FROM books WHERE isbn LIKE :a", {'a': f'%{request.form.get("search")}%'}).fetchall()
        title = db.execute("SELECT * FROM books WHERE title LIKE :a", {'a': f'%{request.form.get("search")}%'}).fetchall()
        author = db.execute("SELECT * FROM books WHERE author LIKE :a", {'a': f'%{request.form.get("search")}%'}).fetchall()
        data = dict({'isbn': isbn, 'title': title, 'author': author})
        return render_template('search.html', data=data, username=session['username'])
    data = {}
    return render_template('search.html', data=data, username=session['username'])


@app.route('/<isbn>', methods=['POST', 'GET'])
def book(isbn):
    if request.method == "POST":
        db.execute('INSERT INTO reviews (review, username, book_isbn) VALUES (:review, :username, :book_isbn)', {'review': request.form.get('review'), 'username': session['username'], 'book_isbn': isbn})
    reviews = db.execute('SELECT * FROM reviews WHERE book_isbn=:isbn', {'isbn': isbn}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "FqiaInArQrrxtHZ4djffQ", "isbns": isbn})
    data = res.json()
    data = data['books'][0]
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()
    return render_template('book.html', dic = data, book=book, username=session['username'], reviews=reviews)


@app.route('/api_documentation', methods=['POST', 'GET'])
def document():
    return render_template('document.html', username=session['username'])


@app.route('/api/isbn/<isbn>', methods=['POST', 'GET'])
def api_isbn(isbn):
    books = db.execute('SELECT * FROM books WHERE isbn LIKE :isbn', {'isbn': f'%{isbn}%'}).fetchall()
    total_api = []
    for book in books:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "FqiaInArQrrxtHZ4djffQ", "isbns": book['isbn']})
        data = res.json()
        data = data['books'][0]
        json_api = {
            'title': book['title'],
            'author': book['author'],
            'year': book['time'],
            'isbn': book['isbn'],
            'review_count': data['reviews_count'],
            'average_score': data['average_rating']
        }
        total_api.append(json_api)
    return jsonify(total_api)


@app.route('/api/title/<title>', methods=['POST', 'GET'])
def api_title(title):
    books = db.execute('SELECT * FROM books WHERE title LIKE :title', {'title': f'%{title}%'}).fetchall()
    total_api = []
    for book in books:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "FqiaInArQrrxtHZ4djffQ", "isbns": book['isbn']})
        data = res.json()
        data = data['books'][0]
        json_api = {
            'title': book['title'],
            'author': book['author'],
            'year': book['time'],
            'isbn': book['isbn'],
            'review_count': data['reviews_count'],
            'average_score': data['average_rating']
        }
        total_api.append(json_api)
    return jsonify(total_api)


@app.route('/api/author/<author>', methods=['POST', 'GET'])
def api_author(author):
    books = db.execute('SELECT * FROM books WHERE author LIKE :author', {'author': f'%{author}%'}).fetchall()
    total_api = []
    for book in books:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "FqiaInArQrrxtHZ4djffQ", "isbns": book['isbn']})
        data = res.json()
        data = data['books'][0]
        json_api = {
            'title': book['title'],
            'author': book['author'],
            'year': book['time'],
            'isbn': book['isbn'],
            'review_count': data['reviews_count'],
            'average_score': data['average_rating']
        }
        total_api.append(json_api)
    return jsonify(total_api)


if __name__ == "__main__":

    app.run(debug=True)