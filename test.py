from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://blofgvuyivhzqq:1e02548824479272dd609c3ea8145f5bbeefda577f5169ade40d73e79250b180@ec2-52-86-33-50.compute-1.amazonaws.com:5432/d1amb8uprcrbvg"


@app.route('/')
def index():
    # x = db.execute('SELECT * FROM test').fetchall()
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('registration.html')