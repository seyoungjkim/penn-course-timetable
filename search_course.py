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
                print(course_data[course])


if __name__ == '__main__':
    search("CHEM-221", DATA_DIRECTORY)
    print("==============================================================================================")
    search("MATH-360", DATA_DIRECTORY)
    print("==============================================================================================")
    search("BIOL-221", DATA_DIRECTORY)
