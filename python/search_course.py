import os
import json

DATA_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/data"


def semester(filename):
    year = 2000 + int(filename[:2])
    season = "Fall" if filename[2] == "C" else "Spring"
    return season + " " + str(year)


# Search a given data directory for course time info
def search(course, directory):
    print("Beginning search for " + course)
    for filename in os.listdir(directory):
        with open(directory + "/" + filename, 'r') as file:
            course_data = json.load(file)
            if course in course_data:
                print("Results from " + semester(filename) + ":")
                print(stringify_course_info(course_data[course]))


def stringify_course_info(course_info_list):
    text = ""
    for class_time in course_info_list:
        text = text + class_time["type"] + " offered on " + class_time["day"] + " at " + class_time["time"] + "\n"
    return text[:-1]


if __name__ == '__main__':
    search("EAS-203", DATA_DIRECTORY)
    print("==============================================================================================")
    search("CIS-380", DATA_DIRECTORY)
    print("==============================================================================================")
    search("NETS-412", DATA_DIRECTORY)
