from app import db
from sqlalchemy.schema import UniqueConstraint

class Course(db.Model):
    __tablename__ = 'courses'
    __table_args__ = (
        UniqueConstraint('department', 'number'),
    )

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String())
    number = db.Column(db.String())
    sections = db.relationship('Section', backref='courses', lazy=True)

    def __init__(self, department, number):
        self.department = department
        self.number = number

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'department': self.department, 
            'number': self.number,
        }


class Semester(db.Model):
    __tablename__ = 'semesters'
    __table_args__ = (
        UniqueConstraint('season', 'year'),
    )

    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    sections = db.relationship('Section', backref='semesters', lazy=True)

    def __init__(self, season, year):
        self.season = season
        self.year = year

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'season': self.season, 
            'year': self.year,
        }

class Section(db.Model):
    __tablename__ = 'sections'
    __table_args__ = (
        UniqueConstraint('course_id', 'semester_id', 'number', 'day', 'time'),
    )

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(), nullable=False)
    day = db.Column(db.String(), nullable=False)
    time = db.Column(db.String(), nullable=False)
    class_format = db.Column(db.String(), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'),
        nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'),
        nullable=False)

    def __init__(self, course_id, semester_id, number, day, time, class_format):
        self.course_id = course_id
        self.semester_id = semester_id
        self.number = number
        self.day = day
        self.time = time
        self.class_format = class_format

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'number': self.number,
            'day': self.day,
            'time': self.time,
            'class_format': self.class_format,
        }
