import psycopg2
import os


TEXT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../raw-text/"
    

def add_all_semesters():
    try:
        connection = psycopg2.connect(database="penn_course_timetable_store")
        cursor = connection.cursor()
        directory = TEXT_DIRECTORY
        results = []
        files = os.listdir(directory)
        files.sort()
        for filename in files:
            season, year = parse_semester(filename)
            add_semester(cursor, season, year)
        connection.commit()
        print("Successfully inserted records into semesters table.")
    except psycopg2.Error as error:
        print("Failed to insert records into semesters table.", error)
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


def add_semester(cursor, season, year):
    query = "INSERT INTO semesters (SEASON, YEAR) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    record = (season, year)
    cursor.execute(query, record)


if __name__ == '__main__':
    add_all_semesters()
