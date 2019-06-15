function displayFormContents() {
    const urlParams = new URLSearchParams(window.location.search);
    if (!(urlParams.has("course"))) {
        return;
    }
    const courseName = parseInput(urlParams.get("course"));
    const courseDataElement = document.getElementById('course-data');
    const courseDataList = [data16C, data17A, data17C, data18A, data18C];
    courseDataElement.innerHTML = getCourseData(courseName, courseDataList);
}

function getCourseData(courseName, courseDataList) {
    let text = "<h2>Results for " + courseName + ":</h2>";
    for (let j = 0; j < courseDataList.length; j++) {
        let courseData = courseDataList[j];
        if (!(courseName in courseData)) {
            continue;
        }
        text += "<h3>" + getSemester(j) +":</h3>";
        const timeList = courseData[courseName];
        for (let i = 0; i < timeList.length; i++) {
            text += "<p>" + timeList[i]["type"] + " " + timeList[i]["section"] + " offered " + timeList[i]["day"] +
                " at " + timeList[i]["time"] + "</p>";
        }
    }
    return text;
}

function parseInput(courseName) {
    let parsedName = courseName;
    if (/([A-Za-z]+)-([0-9]+)/.test(courseName)) {
        parsedName = courseName.toUpperCase();
        return parsedName;
    }
    let array = courseName.match(/([A-Za-z]+)(\s*)([0-9]+)/);
    if (array == null) {
        return parsedName;
    }
    if (array.length >= 4) {
        parsedName = array[1].toUpperCase() + "-" + array[3];
    }
    return parsedName;
}


function getSemester(index) {
    let semester;
    switch (index) {
        case 0:
            semester = "Fall 2016";
            break;
        case 1:
            semester = "Spring 2017";
            break;
        case 2:
            semester = "Fall 2017";
            break;
        case 3:
            semester = "Spring 2018";
            break;
        case 4:
            semester = "Fall 2018";
            break;
        default:
            semester = "Unknown semester"
    }
    return semester
}

displayFormContents();
