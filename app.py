import os
from flask import Flask, render_template, redirect, request, url_for


app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        course = request.form["course"]
        return redirect(url_for('results_page', course=course))
    return render_template('index.html')


@app.route('/sad/<course>', methods=['GET', 'POST'])
def results_page(course):
    if request.method == 'POST':
        course = request.form["course"]
        return redirect(url_for('results_page', course=course))
    return render_template('index.html', course=course)


if __name__ == '__main__':
    app.run(debug=True)
