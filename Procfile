web: gunicorn -b :$PORT app:app --log-file=-
worker: python3 scripts/semester_script.py && python3 scripts/section_script.py
