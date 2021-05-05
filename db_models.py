from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    lectures_count = db.Column(db.Integer, nullable=False)
