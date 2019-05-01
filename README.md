# Penn Course Timetable

The goal is provide an easy way to see Penn course time data from previous semesters for course planning purposes. 
This is currently not part of the Penn Registrar API (https://penn-sdk.readthedocs.io/en/latest/registrar.html).
The data is obtained from parsing PDFs from the course register, which is publicly available at 
https://www.registrar.upenn.edu/archives/index.html.

# Setup
Run `pip install pdfminer` (Python 2) or `pip install pdfminer.six` (Python 3). And check out `search_course.py` to see 
how you can search for a particular course (currently prints raw JSON data).

# TODO
* Create user interface
* Database design (to support lookup by course over multiple semesters)
    * SQLite
* Define API and data structures
* Make parsing more efficient (perhaps look into PDFMiner utils or replace tokenization with another parsing process)
* Fetch and parse older PDFs from Penn Course Register

# Course Data
Example data (see `/data` folder for more):
```
{
  "AFRC-240": [
    {
      "day": "MW",
      "time": "5:30-7:30PM",
      "type": "LEC"
    }
  ],
  "AFRC-248": [
    {
      "day": "W",
      "time": "2-5PM",
      "type": "SEM"
    }
  ],
  "AFRC-269": [
    {
      "day": "MW",
      "time": "3-4PM",
      "type": "LEC"
    },
    {
      "day": "T",
      "time": "4:30-5:30PM",
      "type": "REC"
    },
    {
      "day": "W",
      "time": "4-5PM",
      "type": "REC"
    },
    {
      "day": "R",
      "time": "3:30-4:30PM",
      "type": "REC"
    }
  ]
}
```

# Issues
* Parsing two or three-letter course codes (BE 100 renders as BE -100 in the PDF), and many CIS courses are not being
properly separated

# Solved Issues
* Class types - LEC, REC, LAB, SEM, SRT, STU, CLN, ONL, IND
* Day combinations - instead of hard-coding MW or TR, used a regex that accepts strings which are some combination of 
M, T, W, R, F, S, U
* Page splits - convert entire document to text at once

