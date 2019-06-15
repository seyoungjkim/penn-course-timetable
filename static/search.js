function displayFormContents() {
    const courseDataElement = document.getElementById('course-data');
    console.log(courseDataElement.innerHTML);
    const resultsData = JSON.parse(courseDataElement.innerHTML);
    courseDataElement.innerHTML = displayCourseData(resultsData);
}

function displayCourseData(courseData) {
    let text = "";
    for (const semester in courseData) {
        text += "<h3>" + semester +":</h3>";
        const semesterData = courseData[semester];
        for (let i = 0; i < semesterData.length; i++) {
            const classData = semesterData[i];
            text += "<p>" + classData["type"] + " " + classData["section"] + " offered " + classData["day"] +
                " at " + classData["time"] + "</p>";
        }
    }
    return text;
}

displayFormContents();