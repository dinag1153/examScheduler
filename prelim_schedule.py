import sys
import re
from icalendar import Event, Calendar
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox

import requests
from bs4 import BeautifulSoup

URL = "https://registrar.cornell.edu/exams/fall-prelim-exam-schedule"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

content = soup.find(class_="content").find('pre')

course_entries = []

schedule_data = str(content)

def generate_schedule():

    # Prompt the user to input their enrolled courses
    print("Enter your enrolled courses (one per line), and press Enter twice when you're done:")
    enrolled_courses = [course_entry.get() for course_entry in course_entries]

    while True:
        course_input = input()
        if not course_input:
            break
        enrolled_courses.append(course_input)

    # Create a new iCal calendar
    cal = Calendar()

    # Loop through the schedule data and filter based on enrolled courses
    for line in schedule_data.split('\n'):
        if line.strip():  # Ignore empty lines
            try:
                course, date_str, location = re.split(r'\s{2,}', line.strip())
                # print(f"Course: {course}, Date: {date_str}, Location: {location}")

                # Check if the course is in the list of enrolled courses
                if course in enrolled_courses:
                    # Parse date string
                    date_parts = date_str.split('/')
                    month, day, year = map(int, date_parts)
                    start_time = "19:30"  # 7:30 PM
                    end_time = "21:00"    # 9:00 PM

                    # Create iCal event
                    event = Event()
                    event.add('summary', course)
                    start_datetime = datetime(year, month, day, int(start_time[:2]), int(start_time[3:]))
                    end_datetime = start_datetime + timedelta(hours=1, minutes=30)
                    event.add('dtstart', start_datetime)
                    event.add('dtend', end_datetime)            
                    event.add('location', location)

                    # Add event to the calendar
                    cal.add_component(event)
            except ValueError:
                pass
                #print(f"Skipping line: {line} - Error unpacking values")

    # Save the iCal data to a file
    with open('prelim_schedule.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Success : Course schedule generated and saved as 'prelim_schedule.ics'")

    # Exit the program after success
    sys.exit(0)

app = tk.Tk()
app.title("Prelim Schedule Generator")

frame = ttk.Frame(app)
frame.grid(column=0, row=0, padx=10, pady=10)

generate_button = ttk.Button(frame, text="Generate Schedule", command=generate_schedule)
generate_button.grid(column=0, row=0, padx=10, pady=5)

app.mainloop()
