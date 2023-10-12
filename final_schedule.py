import re
from icalendar import Event, Calendar
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

URL = "https://registrar.cornell.edu/exams/fall-final-exam-schedule"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

content = soup.find(class_="content").find('pre')
schedule_data = str(content)

# Function to get user input for enrolled courses
def get_enrolled_courses():
    print("Enter your enrolled courses (one per line), and press Enter twice when you're done:")
    enrolled_courses = []
    while True:
        course_input = input()
        if not course_input:
            break
        enrolled_courses.append(course_input)
    return enrolled_courses

def generate_schedule(schedule_data, enrolled_courses):
    # Create a new iCal calendar
    cal = Calendar()

    # Loop through the schedule data and filter based on enrolled courses
    for line in schedule_data.split('\n'):
        if line.strip():  # Ignore empty lines
            try:
                course, date_str, *time_parts, description = re.split(r'\s{2,}', line.strip())
                course = " ".join(course.split()[:2])
                time_str = " ".join(time_parts)

                # Check if "AM" or "PM" is included in the time string
                ampm = "AM" if "AM" in time_str else "PM"

                # Remove "AM" or "PM" from the time string
                time_str = time_str.replace("AM", "").replace("PM", "")

                # Convert to 24-hour format if needed
                if ampm == "PM" and "12:" not in time_str:
                    hours, minutes = map(int, time_str.split(':'))
                    hours += 12
                    time_str = f"{hours:02d}:{minutes:02d}"

                start_time = time_str

                # Check if the course is in the list of enrolled courses
                if course in enrolled_courses:
                    # Parse date and time
                    date_parts = date_str.split('/')
                    month, day, year = map(int, date_parts)
                    time_parts = start_time.split(':')
                    hour, minute = int(time_parts[0]), int(time_parts[1])

                    # Create iCal event
                    event = Event()
                    event.add('summary', course)
                    event.add('description', description)
                    start_datetime = datetime(year, month, day, hour, minute)
                    end_datetime = start_datetime + timedelta(hours=2, minutes=30)  # Exams last 2.5 hours
                    event.add('dtstart', start_datetime)
                    event.add('dtend', end_datetime)

                    # Add event to the calendar
                    cal.add_component(event)
            except ValueError:
                pass

    # Save the iCal data to a file
    with open('final_exam_schedule.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Success: Final exam schedule generated and saved as 'final_exam_schedule.ics'")

if __name__ == "__main__":
    enrolled_courses = get_enrolled_courses()
    generate_schedule(schedule_data, enrolled_courses)
