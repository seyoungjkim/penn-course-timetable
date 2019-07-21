import os
import json
import re

DATA_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../data"

# Test utils
def search(course, directory):
    print("Beginning search for " + course)
    results = ""
    for filename in os.listdir(directory):
        with open(directory + "/" + filename, 'r') as file:
            course_data = json.load(file)
            if course in course_data:
                results += print("Results from " + semester(filename) + ":")
                results += print(stringify_course_info(course_data[course]))
    return results


def stringify_course_info(course_info_list):
    text = ""
    for class_time in course_info_list:
        text = text + class_time["type"] + class_time["section"] + " offered on " + class_time["day"] + " at " + \
               class_time["time"] + "\n"
    return text[:-1]


# App utils
def search_json(course):
    directory = DATA_DIRECTORY
    results = []
    files = os.listdir(directory)
    files.sort()
    for filename in files:
        with open(directory + "/" + filename, 'r') as file:
            course_data = json.load(file)
            if course in course_data:
                results.append({"semester": semester(filename), "data": course_data[course]})
    return results


def semester(filename):
    year = 2000 + int(filename[:2])
    if filename[2] == "A":
        season = "Spring"
    elif filename[2] == "B":
        season = "Summer"
    else:
        season = "Fall"
    return season + " " + str(year)


def parse_input(user_input):
    if re.match('^[A-Za-z]{2,4}-[0-9]{3}$', user_input):
        return user_input.upper()
    elif re.match('^[A-Za-z]{2,4} [0-9]{3}$', user_input):
        return user_input[:-4].upper() + '-' + user_input[-3:]
    elif re.match('^[A-Za-z]{2,4}[0-9]{3}$', user_input):
        return user_input[:-3].upper() + '-' + user_input[-3:]
    else:
        return "NotFound"