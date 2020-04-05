import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, time in reader:
        db.execute("INSERT INTO books (isbn, title, author, time) VALUES (:isbn, :title, :author, :time)",
                    {"isbn": isbn, "title": title, "author": author, "time":time})
    db.commit()


if __name__ == "__main__":
    main()
