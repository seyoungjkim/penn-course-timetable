from app import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String())

    def __init__(self, course_name):
        self.course_name = course_name

    def __repr__(self):
        return '<id {}>'.format(self.id)
