# Exam Schedule Generator

This is a Python script turned into an executable that allows users to generate iCalendar (ICS) files for their course exam schedules. The script scrapes exam schedules from the Cornell University Registrar's website and creates separate ICS files for prelim and final exams to be imported into Google Calendar.

## Features

- Generates ICS files for both preliminary and final exam schedules.
- Filters exams based on the user's enrolled courses.
- Supports fall and spring semesters.
- Differentiates between preliminary and final exams for correct event duration and description.

## Prerequisites

If you're using the provided executable, you don't need to install Python separately. Otherwise, before using this script, you need to have Python installed on your system.

## Usage

1. Download and run the executable titled "exam_schedule.exe".
2. Select the exam type (prelim or final).
3. Enter the semester (fall or spring).
4. Input your enrolled courses in the format "COURSE CODE COURSE NUMBER" (e.g., PHYS 1234). Press Enter twice when you're done.
5. The script generates an ICS file with your exam schedule in the current directory, most likely your downloads folder if not moved.
6. The ICS file can be imported into any existing Google Calendar calendar or any other compatible calendar application of your choice.

## Acknowledgments

- The script was created by Dina Gamous for fellow Google Calendar obsessed Cornell students.

## Support

If you encounter any issues or have questions, please create an issue in the GitHub repository.

