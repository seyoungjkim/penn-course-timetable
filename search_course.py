import os
import json

DATA_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/data"


# Search a given data directory for course time info
def search(course, directory):
    for filename in os.listdir(directory):
        with open(directory + "/" + filename, 'r') as file:
            course_data = json.load(file)
            if course in course_data:
                print(filename)
                print(course_data[course])


if __name__ == '__main__':
    search("ACCT-613", DATA_DIRECTORY)
    search("MATH-360", DATA_DIRECTORY)
