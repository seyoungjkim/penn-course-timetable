import re
from python.pdf_parser import extract_text


# Returns JSON representation of course time info
def get_course_info(pdf_path):
    page_text = extract_text(pdf_path)
    tokens = page_text.split()
    time_info = parse_register(tokens)
    course_data = associate_time_with_course(time_info)
    return course_data


# Parse course register text info for all course, day, and time tokens
def parse_register(tokens):
    time_info = []
    i = 0
    while i < len(tokens):
        if is_course_code(tokens[i]):
            time_info.append(tokens[i])
            i = i + 1
        elif is_dangling_course_number(tokens[i]) and i > 0:
            time_info.append((tokens[i - 1] + tokens[i]))
            i = i + 1
        elif is_class_type(tokens[i]) and i > 0:
            # check for cross-listing
            listed = False
            time_info.append(tokens[i - 1])
            time_info.append(tokens[i])
            i = i + 1
            while i < len(tokens):
                if tokens[i] == "LISTED:":
                    listed = True
                if tokens[i] == "LIST:":
                    listed = False
                if is_class_type(tokens[i]):
                    break
                if (is_course_code(tokens[i]) or is_dangling_course_number(tokens[i])) and not listed:
                    break
                if is_day(tokens[i]) or is_time(tokens[i]):
                    time_info.append(tokens[i])
                i = i + 1
        else:
            i = i + 1
    return time_info


# Create structured data from a list of course, day, and time info and
def associate_time_with_course(course_time_list):
    course_data = {}
    i = 0
    while i < len(course_time_list):
        if is_course_code(course_time_list[i]):
            # handle cross-listed courses
            if i + 1 < len(course_time_list) and is_course_code(course_time_list[i + 1]):
                i = i + 1
                continue
            key = course_time_list[i]
            if key in course_data:
                times = course_data[key]
            else:
                times = []
                course_data[key] = times
            i = i + 1
            while i < len(course_time_list) and not is_course_code(course_time_list[i]):
                if i > 0 and i + 1 < len(course_time_list) and is_class_type(course_time_list[i]) and \
                        course_time_list[i + 1] == "TBA":
                    section = course_time_list[i - 1]
                    if not is_section(section):
                        section = ""
                    class_info = {
                        "section": section,
                        "day": "TBA",
                        "time": "TBA",
                        "type": course_time_list[i]
                    }
                    if not is_section(section):
                        i = i + 2
                    else:
                        i = i + 3
                    for t in times:
                        if t["section"] == section:
                            break
                    times.append(class_info)
                elif i > 0 and i + 2 < len(course_time_list) and is_class_type(course_time_list[i]) and \
                        is_day(course_time_list[i + 1]) and is_time(course_time_list[i + 2]):
                    section = course_time_list[i - 1]
                    if not is_section(section):
                        section = ""
                    class_info = {
                        "section": section,
                        "day": course_time_list[i + 1],
                        "time": course_time_list[i + 2],
                        "type": course_time_list[i]
                    }
                    if not is_section(section):
                        i = i + 2
                    else:
                        i = i + 3
                    for t in times:
                        if t["section"] == section:
                            break
                    times.append(class_info)
                else:
                    i = i + 1

        else:
            i = i + 1
    return course_data


def is_course_code(token):
    if re.match('^[A-Z]{2,4}-[0-9]{3}$', token):
        return True
    else:
        return False


# Cases such as BE  -100, CIS -520
def is_dangling_course_number(token):
    if re.match('^-[0-9]{3}$', token):
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


def is_section(token):
    if re.match('[0-9]{3}', token):
        return True
    else:
        return False


def is_class_type(token):
    types = {"LEC", "REC", "LAB", "SEM", "SRT", "STU", "CLN", "ONL", "IND", "DIS"}
    if token in types:
        return True
    else:
        return False
