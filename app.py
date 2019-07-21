import os
import re
from lib.search_course import search_json, parse_input
from flask import Flask, render_template, redirect, request, url_for, Markup


app = Flask(__name__)


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
    raw_results = search_json(parsed_course)
    rendered_results = display_results(raw_results)
    return render_template('index.html', course=parsed_course, results=rendered_results)


def display_results(raw_results):
    text = ""
    for semesterData in raw_results:
        text += "<h3>" + semesterData["semester"] + ":</h3>"
        courseData = semesterData["data"]
        for classData in courseData:
            text += "<p>" + classData["type"] + " " + classData["section"] + \
                " offered " + classData["day"] + \
                    " at " + classData["time"] + "</p>"
    return Markup(text)


if __name__ == '__main__':
    app.run(debug=True)
