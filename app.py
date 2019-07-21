import os
import re
from lib.search_course import parse_input
from flask import Flask, render_template, redirect, request, url_for, Markup
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models import *


@app.route('/', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        course = request.form["course"]
        return redirect(url_for('results_page', course=course))
    return render_template('index.html')


@app.route('/course/<course>', methods=['GET', 'POST'])
def results_page(course):
    if request.method == 'POST':
        course = request.form["course"]
        return redirect(url_for('results_page', course=course))
    parsed_course = parse_input(course)
    raw_results = get_results(parsed_course)
    rendered_results = display_results(raw_results)
    return render_template('index.html', course=parsed_course, results=rendered_results)


def get_results(course_name):
    semesters = Semester.query.all()
    results = []
    department, number = parse_course(course_name)
    for semester in semesters:
        semester_name = semester.season + " " + str(semester.year)
        semester_course_data = get_sections(semester, department, number)
        results.append({"semester": semester_name, "data": semester_course_data})
    return results


def get_sections(semester, department, number):
    course = Course.query.filter_by(department=department, number=number).first()
    if course is None:
        return []
    semester_id = semester.serialize()["id"]
    course_id = course.serialize()["id"]
    sections = Section.query.filter_by(semester_id=semester_id, course_id=course_id)
    return [section.serialize() for section in sections]
    

def parse_course(course_name):
    department = course_name[:-4]
    number = course_name[-3:]
    return department, number


def display_results(raw_results):
    text = ""
    for semester_data in raw_results:
        text += display_section_for_semester(semester_data["semester"], semester_data["data"])
    return Markup(text)


def display_section_for_semester(semester, course_data):
    if len(course_data) == 0:
        return ""
    text = "<h3>" + semester + ":</h3>"
    for section in course_data:
        text += display_section(section["class_format"], section["number"], section["day"], section["time"])
    return text


def display_section(course_format, number, day, time):
    return "<p>" + course_format + " " + number + " offered " + day + " at " + time + "</p>"


if __name__ == '__main__':
    app.run()
