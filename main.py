import json
import datetime
import pandas as pd
from BCS import BootcampSpot

students = pd.read_csv('data/active_students.csv')["name"].tolist()
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
        if x in students:
            print(x)
            missing += 1
    print(f'\nStudents not checked in: {missing}\n')
    print('=' * 100)

def check_total_absences():
    """
    Ping PCS API and print the names of all students and their associated absences
    :return: None
    """
    df = bcs.get_absences_df()
    df = df.loc[df['name'].isin(students)]
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


def main():
    check_attendance_today()
    check_nearest_assignment_submission()
    check_total_absences()

if __name__ == "__main__":
    main()
