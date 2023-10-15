import sys, re
from icalendar import Event, Calendar
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

def get_schedule_url(exam_type, semester):
    base_url = "https://registrar.cornell.edu/exams/"
    semester_url = f"{semester}-final-exam-schedule" if exam_type == "final" else f"{semester}-prelim-exam-schedule"
    return f"{base_url}{semester_url}"

def get_schedule_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find(class_="content").find('pre')
    schedule_data = str(content)
    return schedule_data

def generate_schedule(enrolled_courses, semester, exam_type):
    url = get_schedule_url(exam_type, semester)
    schedule_data = get_schedule_data(url)

    cal = Calendar()
    added_courses = set()

    for line in schedule_data.split('\n'):
        if line.strip():
            try:
                if exam_type == "final":
                    course, date_str, *time_parts, description = re.split(r'\s{2,}', line.strip())
                    course = " ".join(course.split()[:2])
                    time_str = " ".join(time_parts)

                    ampm = "AM" if "AM" in time_str else "PM"
                    time_str = time_str.replace("AM", "").replace("PM", "")

                    if ampm == "PM" and "12:" not in time_str:
                        hours, minutes = map(int, time_str.split(':'))
                        hours += 12
                        time_str = f"{hours:02d}:{minutes:02d}"

                    start_time = time_str
                else:
                    course, date_str, location = re.split(r'\s{2,}', line.strip())
                    start_time = "19:30"

                if course in enrolled_courses and (course not in added_courses or exam_type == "prelim"):
                    date_parts = date_str.split('/')
                    month, day, year = map(int, date_parts)
                    time_parts = start_time.split(':')
                    hour, minute = int(time_parts[0]), int(time_parts[1])

                    event = Event()
                    event.add('summary', course)
                    if exam_type == "final":
                        event.add('description', description)
                        end_datetime = datetime(year, month, day, hour, minute) + timedelta(hours=2, minutes=30)
                    else:
                        end_datetime = datetime(year, month, day, hour, minute) + timedelta(hours=1, minutes=30)
                        event.add('location', location)
                    event.add('dtstart', datetime(year, month, day, hour, minute))
                    event.add('dtend', end_datetime)
                    cal.add_component(event)
                    if exam_type == "final":
                        added_courses.add(course)
            except ValueError:
                pass

    filename = f'{semester}_{exam_type}_exam_schedule.ics'
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    print(f"Success: {semester} {exam_type} exam schedule generated and saved as '{filename}'")
    sys.exit(0)

def menu():
    exam_type = input("Select exam type (prelim/final): ").lower()
    if exam_type not in ["prelim", "final"]:
        print("Invalid exam type. Please enter 'prelim' or 'final'.")
        sys.exit(1)

    semester = input("Enter the semester (fall/spring): ").lower()
    if semester not in ["fall", "spring"]:
        print("Invalid semester. Please enter 'fall' or 'spring'.")
        sys.exit(1)

    enrolled_courses = get_enrolled_courses()
    generate_schedule(enrolled_courses, semester, exam_type)

def get_enrolled_courses():
    print("Enter your enrolled courses in the form PHYS 1234 (one per line), and press Enter twice when you're done:")
    enrolled_courses = []
    while True:
        course_input = input().strip().upper()
        if not course_input:
            break
        enrolled_courses.append(course_input)
    return enrolled_courses

if __name__ == "__main__":
    menu()