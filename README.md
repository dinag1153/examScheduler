# examScheduler
Create ical files to import Cornell exams into personal Google Calendar

# How to use:
# No python required:
Download the final_schedule.exe file. Click on the file downloaded and follow the instructions on the terminal that opens. Make sure the inputed courses follow the form PHYS 1234. After double entering, a file in the same folder as the final_schedule.exe file, most likely your downloads folder, will be created with the name final_exam_schedule.ics. In google calender, import this file to any existing calendar.


# Using python:
Download the desired file (prelim_schedule or final_schedule). 
Have python installed. 
Open terminal and cd into the folder where the python file is located on your local computer, probably the downloads folder. 
If you have not already, run "pip install icalendar". 
Run "python prelim_schedule.py" or "python final_schedule.py" based on the file downloaded. 
Import your course names in the form of PHYS 1234. 
The ical file will be created in the same folder as the python script. 
In google calendar, import the ical file into any existing calendar. 
