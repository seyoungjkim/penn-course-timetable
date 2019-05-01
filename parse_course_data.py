import re
import json
from pdf_text_parser import extract_text_by_page


# TODO: refactor, look into PDFMiner utilities
def get_course_info(pdf_path):
    course_data = {}
    for page_text in extract_text_by_page(pdf_path):
        tokens = page_text.split()
        time_info = []
        i = 0
        while i < len(tokens):
            if is_course_code(tokens[i]) and i - 1 > 0 and tokens[i - 1] != "LISTED:":
                time_info.append(tokens[i])
                i = i + 1
            elif is_class_type(tokens[i]):
                i = i + 1
                while i < len(tokens):
                    if is_course_code(tokens[i]) or is_class_type(tokens[i]):
                        break
                    if is_day(tokens[i]) or is_time(tokens[i]):
                        time_info.append(tokens[i])
                    i = i + 1
            else:
                i = i + 1
        i = 0
        while i < len(time_info):
            if is_course_code(time_info[i]):
                if i + 1 < len(time_info) and is_course_code(time_info[i + 1]):
                    i = i + 1
                    continue
                key = time_info[i]
                times = []
                i = i + 1
                while i < len(time_info) and not is_course_code(time_info[i]):
                    if i + 1 < len(time_info) and is_day(time_info[i]) and is_time(time_info[i + 1]):
                        times.append(time_info[i])
                        times.append(time_info[i + 1])
                        i = i + 2
                    else:
                        i = i + 1
                course_data[key] = times
            else:
                i = i + 1
    return course_data


def is_course_code(token):
    if re.match('^[A-Z]{3,4}-[0-9]{3}$', token):
        return True
    else:
        return False


def is_day(token):
    days = set(["M", "T", "W", "R", "F", "MW", "MWF", "TR"])
    if token in days:
        return True
    else:
        return False


# TODO: combine regular expressions
def is_time(token):
    if re.match('[0-9]{1,2}-[0-9]{1,2}', token):
        return True
    elif re.match('[0-9]{1,2}:[0-9]{2}-[0-9]{1,2}', token):
        return True
    elif re.match('[0-9]{1,2}-[0-9]{1,2}:[0-9]{2}', token):
        return True
    elif re.match('[0-9]{1,2}:[0-9]{2}-[0-9]{1,2}:[0-9]{2}', token):
        return True
    else:
        return False


def is_class_type(token):
    types = set(["SEM", "LEC", "REC"])
    if token in types:
        return True
    else:
        return False


if __name__ == '__main__':
    f = open("course_data.txt", "w")
    f.write(json.dumps(get_course_info("sample.pdf"), indent=2))
    f.close()
