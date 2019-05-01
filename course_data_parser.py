import re
from pdf_parser import extract_text


# Returns JSON representation of course time info
def get_course_info(pdf_path):
    page_text = extract_text(pdf_path)
    tokens = page_text.split()
    time_info = parse_register(tokens)
    course_data = associate_time_with_course(time_info)
    return course_data


# Parse course register text info
def parse_register(tokens):
    time_info = []
    i = 0
    while i < len(tokens):
        if is_course_code(tokens[i]) and i - 1 > 0 and tokens[i - 1] != "LISTED:":
            time_info.append(tokens[i])
            i = i + 1
        elif is_class_type(tokens[i]):
            time_info.append(tokens[i])
            i = i + 1
            while i < len(tokens):
                if is_course_code(tokens[i]) or is_class_type(tokens[i]):
                    break
                if is_day(tokens[i]) or is_time(tokens[i]):
                    time_info.append(tokens[i])
                i = i + 1
        else:
            i = i + 1
    return time_info


# Traverse a list of course and time info
def associate_time_with_course(course_time_list):
    course_data = {}
    i = 0
    while i < len(course_time_list):
        if is_course_code(course_time_list[i]):
            # cross-listed courses
            if i + 1 < len(course_time_list) and is_course_code(course_time_list[i + 1]):
                i = i + 1
                continue
            key = course_time_list[i]
            times = []
            i = i + 1
            while i < len(course_time_list) and not is_course_code(course_time_list[i]):
                if i + 1 < len(course_time_list) and is_class_type(course_time_list[i]) and \
                        course_time_list[i + 1] == "TBA":
                    class_info = {
                        "day": "TBA",
                        "time": "TBA",
                        "type": course_time_list[i]
                    }
                    times.append(class_info)
                    i = i + 2
                elif i + 2 < len(course_time_list) and is_class_type(course_time_list[i]) and \
                        is_day(course_time_list[i + 1]) and is_time(course_time_list[i + 2]):
                    class_info = {
                        "day": course_time_list[i + 1],
                        "time": course_time_list[i + 2],
                        "type": course_time_list[i]
                    }
                    times.append(class_info)
                    i = i + 3
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
    if re.match('^[M,T,W,R,F,S,U]+$', token):
        return True
    else:
        return False


# TODO: combine regular expressions
def is_time(token):
    if token == "TBA":
        return True
    elif re.match('[0-9]{1,2}-[0-9]{1,2}', token):
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
