# Exam Schedule Generator

This is a Python script turned into an executable that allows users to generate iCalendar (ICS) files for their course exam schedules. The script scrapes exam schedules from the Cornell University Registrar's website and creates separate ICS files for prelim and final exams to be imported into Google Calendar.
Most easily used through Google Colab: https://colab.research.google.com/drive/1eEBoLhFMpWD5JqpCx1nHJ-cGyaDslXMr?usp=sharing

## Features

- Generates ICS files for both preliminary and final exam schedules.
- Filters exams based on the user's enrolled courses.
- Supports fall and spring semesters.
- Differentiates between preliminary and final exams for correct event duration and description.

## Prerequisites

Before using this script, you need to have Python installed on your system. Also run the following command before executing the script for the first time: 
pip install icalendar

## Usage

1. Download "exam_schedule.py". "exam_schedule.exe", although not requiring python, may not work on every computer.
2. Open your terminal and make sure you are in the path that contains the file you just downloaded (will probably be your downloads folder)
3. Run the following command: python exam_schedule.py
4. Select the exam type (prelim or final).
5. Enter the semester (fall or spring).
6. Input your enrolled courses in the format "COURSE CODE COURSE NUMBER" (e.g., PHYS 1234). Press Enter twice when you're done.
7. The script generates an ICS file with your exam schedule in the current directory, most likely your downloads folder if not moved.
8. The ICS file can be imported into any existing Google Calendar calendar or any other compatible calendar application of your choice.

## Acknowledgments

- The script was created by Dina Gamous for fellow Google Calendar obsessed Cornell students.

## Support

If you encounter any issues or have questions, please create an issue in the GitHub repository.

