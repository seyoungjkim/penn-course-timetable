import re


# Returns JSON representation of course time info
def get_course_info(txt_path):
    with open(txt_path, "r") as file:
        page_text = file.read()
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
            cross_listed = False
            j = 1
            section = tokens[i - j]
            while not is_section(section):
                j += 1
                section = tokens[i - j]
            time_info.append(section)  # section info
            time_info.append(tokens[i])  # class type
            i = i + 1
            while i < len(tokens):
                if tokens[i] == "LISTED:":
                    cross_listed = True
                if tokens[i] == "LIST:":
                    cross_listed = False
                if is_class_type(tokens[i]):
                    break
                # check for cross-listing
                if (is_course_code(tokens[i]) or is_dangling_course_number(tokens[i])) and not cross_listed:
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
                        section = times[-1]["section"]
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
                    times.append(class_info)
                elif i > 0 and i + 2 < len(course_time_list) and is_class_type(course_time_list[i]) and \
                        is_day(course_time_list[i + 1]) and is_time(course_time_list[i + 2]):
                    section = course_time_list[i - 1]
                    if not is_section(section):
                        print(key)
                        print(course_time_list[i])
                        section = times[-1]["section"]
                    day = course_time_list[i + 1]
                    time = course_time_list[i + 2]
                    course_type = course_time_list[i]
                    class_info = {
                        "section": section,
                        "day": day,
                        "time": time,
                        "type": course_type
                    }
                    if not is_section(section):
                        i = i + 2
                    else:
                        i = i + 3
                    is_duplicate_time = False
                    for t in times:
                        if t["day"] == day and t["time"] == time and t["section"] == section:
                            is_duplicate_time = True
                            break
                    if not is_duplicate_time: times.append(class_info)
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
    types = {"LEC", "REC", "LAB", "SEM", "SRT", "STU", "CLN", "ONL", "IND", "DIS", "MST", "CRT"}
    if token in types:
        return True
    else:
        return False
