import os
import re
from scripts.search_course import search_json
from flask import Flask, render_template, redirect, request, url_for


app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])


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
    results = search_json(parsed_course)
    return render_template('index.html', course=parsed_course, results=results)


def parse_input(user_input):
    if re.match('^[A-Za-z]{2,4}-[0-9]{3}$', user_input):
        return user_input.upper()
    elif re.match('^[A-Za-z]{2,4} [0-9]{3}$', user_input):
        return user_input[:-4].upper() + '-' + user_input[-3:]
    else:
        return "NotFound"


if __name__ == '__main__':
    app.run(debug=True)
