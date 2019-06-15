import os
import json

DATA_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../data"


def semester(filename):
    year = 2000 + int(filename[:2])
    if filename[2] == "A":
        season = "Spring"
    elif filename[2] == "B":
        season = "Summer"
    else:
        season = "Fall"
    return season + " " + str(year)


# Search a given data directory for course time info
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


def search_json(course):
    directory = DATA_DIRECTORY
    results = {}
    for filename in os.listdir(directory):
        with open(directory + "/" + filename, 'r') as file:
            course_data = json.load(file)
            if course in course_data:
                results[semester(filename)] = course_data[course]
    return json.dumps(results)


def stringify_course_info(course_info_list):
    text = ""
    for class_time in course_info_list:
        text = text + class_time["type"] + class_time["section"] + " offered on " + class_time["day"] + " at " + \
               class_time["time"] + "\n"
    return text[:-1]


if __name__ == '__main__':
    search("EAS-203", DATA_DIRECTORY)
    print("==============================================================================================")
    search("CIS-380", DATA_DIRECTORY)
    print("==============================================================================================")
    search("PHYS-170", DATA_DIRECTORY)
