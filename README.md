# Penn Course Timetable

The goal is provide an easy way to see Penn course time data from previous semesters for course planning purposes. 
This is currently not part of the Penn Registrar API (https://penn-sdk.readthedocs.io/en/latest/registrar.html).
The data is obtained from parsing PDFs from the course register, which is publicly available at 
https://www.registrar.upenn.edu/archives/index.html.

# Setup
Run `pip install pdfminer` (Python 2) or `pip install pdfminer.six` (Python 3).

# TODO
* Database design (to support lookup by course over multiple semesters)
    * SQLite
* Define API and data structures
* Make parsing more efficient (perhaps look into PDFMiner utils or replace tokenization with another parsing process)
* Fetch all data from Penn Course Register
* Download and parse all PDFs from web, check for missing data

# Course Data
Example data: 
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

# Possible Issues
* More class types than LEC, SEM, REC?
