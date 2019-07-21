from app import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String())
    number = db.Column(db.Integer)
    sections = db.relationship('Section', backref='courses', lazy=True)

    def __init__(self, department, number):
        self.department = department
        self.number = number

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Semester(db.Model):
    __tablename__ = 'semesters'

    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String())
    year = db.Column(db.Integer)
    sections = db.relationship('Section', backref='semesters', lazy=True)

    def __init__(self, season, year):
        self.season = season
        self.year = year

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'season': self.season, 
            'year': self.year,
        }

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    day = db.Column(db.String())
    time = db.Column(db.String())
    class_format = db.Column(db.String())
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'),
        nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'),
        nullable=False)

    def __init__(self, course, semester, number, day, time, class_format):
        self.course = course
        self.semester = semester
        self.number = number
        self.day = day
        self.time = time
        self.class_format = class_format

    def __repr__(self):
        return '<id {}>'.format(self.id)