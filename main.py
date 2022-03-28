import json
import datetime

import pandas as pd

from BCS import BootcampSpot

# Confirmed students that are not a part of the class. IF THEY JOIN REMOVE THEIR NAME
nan_students = ['Susanna Tabangay','Trinity Guevara','Tyler Sheard', 'William Wright']
# Create the bcs object
bcs = BootcampSpot()


def check_attendance_today():
    """
    Ping BCS API and find out who has not checked into today's class
    :return: None
    """
    df = bcs.get_today_attendance()
    df = df.fillna(value=False)

    # Check present students
    print(f'\nStudents checked in: {len(bcs.get_present_students_dict(df)["present"])}')
    for x in bcs.get_present_students_dict(df)["present"]:
        print(f'\t{x} is present')

    print('='*50)

    # Check missing students
    missing = 0
    for x in bcs.get_present_students_dict(df)["absent"]:
        if x not in nan_students:
            print(f'\t{x} is not checked in')
            missing += 1
    print(f'\nStudents not checked in: {missing}\n')
    print('=' * 100)

def check_total_absences():
    """
    Ping PCS API and print the names of all students and their associated absences
    :return: None
    """
    df = bcs.get_absences_df()
    df = df.loc[~df['name'].isin(nan_students)]
    print(df)
    print('=' * 100)

def check_nearest_assignment_submission():
    """
        Ping BCS API to check and see who has submitted the next assignment.
        :return: None
        """
    assignment = ""
    for x in bcs.get_assignments()["calendarAssignments"]:
        if x['contextId'] == 1 and datetime.date.fromisoformat(x['dueDate'][:10]) >= datetime.date.today():
            assignment = x["title"]
            break
    print(json.dumps(bcs.get_next_homework_submission_dict(bcs.get_specific_grades_df(assignment)),indent=4))
    print('=' * 100)


check_attendance_today()
check_nearest_assignment_submission()
check_total_absences()