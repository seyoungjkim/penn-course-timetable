import psycopg2
import os
import json


DATA_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../data/"
    

# TODO: would likely be cleaner as a class or split into utils
def add_all_sections():
    try:
        connection = psycopg2.connect(database="penn_course_timetable_store")
        cursor = connection.cursor()
        directory = DATA_DIRECTORY
        results = []
        files = os.listdir(directory)
        files.sort()
        for filename in files:
            season, year = parse_semester(filename)
            semester_id = get_semester(cursor, connection, season, year)
            with open(directory + "/" + filename, 'r') as file:
                semester_data = json.load(file)
                for course_name in semester_data:
                    department, number = parse_course(course_name)
                    add_course(cursor, department, number)
                    course_id = get_course(cursor, connection, department, number)
                    sections = semester_data[course_name]
                    for section in sections:
                        add_section(
                            cursor, 
                            course_id, 
                            semester_id, 
                            section["section"],
                            section["day"],
                            section["time"],
                            section["type"]
                        )
                connection.commit()
        print("Successfully inserted records into courses and sections tables.")
    except psycopg2.Error as error:
        print("Failed to insert records into courses and sections tables.", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")


def parse_semester(filename):
    year = 2000 + int(filename[:2])
    if filename[2] == "A":
        season = "Spring"
    elif filename[2] == "B":
        season = "Summer"
    else:
        season = "Fall"
    return season, year


def parse_course(course_name):
    department = course_name[:-4]
    number = course_name[-3:]
    return department, number


def get_course(cursor, connection, department, number):
    query = "SELECT id FROM courses WHERE department=%s and number=%s"
    record = (department, number)
    cursor.execute(query, record)
    return cursor.fetchone()


def get_semester(cursor, connection, season, year):
    query = "SELECT id FROM semesters WHERE season=%s and year=%s"
    record = (season, year)
    cursor.execute(query, record)
    return cursor.fetchone()


def add_course(cursor, department, number):
    query = "INSERT INTO courses (department, number) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    record = (department, number)
    cursor.execute(query, record)


def add_section(cursor, course_id, semester_id, number, day, time, class_format):
    query = "INSERT INTO sections (course_id, semester_id, number, day, time, class_format) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
    record = (course_id, semester_id, number, day, time, class_format)
    cursor.execute(query, record)


if __name__ == '__main__':
    add_all_sections()
