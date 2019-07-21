# Penn Course Timetable

The goal is provide an easy way to see Penn course time data from previous semesters for course planning purposes. 
This is currently not part of the Penn Registrar API (https://penn-sdk.readthedocs.io/en/latest/registrar.html).
The data is obtained from parsing PDFs from the course register, which is publicly available at 
https://www.registrar.upenn.edu/archives/index.html. View at https://www.seyoungkim.com/penn-course-timetable or follow
setup instructions to run locally.

# Setup
Clone the repo. Run `pip install -r requirements.txt` to install requirements for the app.

Download the desired course timetable PDFs and place in the `/bin` folder. 
Run `pip install .`, `python scripts/extract_text_pdf_script.py` (can take quite a while), and `python scripts/data_extraction_script.py` to parse the data.

Run `python app.py` to start the app.

# TODO
* Testing!
* Create better user interface and prettier design (with autocomplete, etc.)
* Add database (currently uses JSON files)
* Define API and data structures
* Make parsing more efficient (perhaps look into PDFMiner utils or replace tokenization with another parsing process)
* Refactor code

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

# Solved Issues
* Duplicate sections
* Cross-listing
* Parsing two or three-letter course codes (BE 100 renders as BE -100 in the PDF), and many CIS courses are not being
properly separated
* Class types - LEC, REC, LAB, SEM, SRT, STU, CLN, ONL, IND
* Day combinations - instead of hard-coding combinations like MW or TR, used a regex that accepts strings which are some combination of 
M, T, W, R, F, S, U
* Page splits - convert entire document to text at once

# Future Directions
* Integrate into some kind of scheduler or course planning tool
