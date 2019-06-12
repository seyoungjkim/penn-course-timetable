import json
import os
from scripts.course_data_parser import get_course_info

TEXT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../raw-text/"
DATA_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../data/"
MISSING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../data/"


# Parse the given course timetable PDF and identify any courses that are missing time data
def find_missing_course_data(pdf_path):
    missing_courses = []
    course_data = get_course_info(pdf_path)
    for course in course_data:
        times_list = course_data[course]
        if len(times_list) == 0:
            missing_courses.append(course)
    return missing_courses, course_data


# Write extracted data to a file as well as course codes that are missing time data, if they exist
def extract_and_write_course_data(pdf_path, output_path, missing_path, variable):
    missing_courses, course_data = find_missing_course_data(pdf_path)
    with open(output_path, "w+") as file:
        file.write(json.dumps(course_data, indent=2))
    if len(missing_courses) > 0:
        with open(missing_path, "w+") as file:
            for course in missing_courses:
                file.write(course + "\n")


if __name__ == '__main__':
    print("Removing existing files...")
    for filename in os.listdir(DATA_DIRECTORY):
        os.remove(DATA_DIRECTORY + "/" + filename)
    for filename in os.listdir(TEXT_DIRECTORY):
        print("Starting to parse " + filename)
        extract_and_write_course_data(
            TEXT_DIRECTORY + filename,
            DATA_DIRECTORY + filename[:3] + "-data.json",
            MISSING_DIRECTORY + filename[:3] + "-missing.txt",
            filename[:3]
        )
