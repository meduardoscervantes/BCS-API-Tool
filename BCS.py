import requests
import config
import pandas as pd
import datetime
pd.set_option('display.max_columns', None)

BASE_URL = "https://bootcampspot.com/api/instructor/v1/"
EMAIL = config.EMAIL
PASSWORD = config.BCS_PASSWORD
COURSE_ID = config.COURSE_ID
ENROLLMENT_ID = config.ENROLLMENT_ID


def make_df(data: list):
    students = dict()
    for x in data:
        keys = list(x.keys())
        values = list(x.values())
        for y in range(len(keys)):
            try:
                if len(students[keys[y]]) > 0:
                    students[keys[y]].append(values[y])
            except KeyError:
                students[keys[y]] = list()
                students[keys[y]].append(values[y])
    return pd.DataFrame(students)


class BootcampSpot:
    def __init__(self):
        """
        __init__ define auth token on back end
        """
        self.auth_token = None
        self.login()

    def login(self) -> None:
        """
        initiate the auth_token
        :return: Does not have a return value
        """
        endpoint = "login"
        response = requests.post(BASE_URL + endpoint, json={'EMAIL': EMAIL, 'password': PASSWORD})
        response.raise_for_status()
        self.auth_token = response.json().get("authenticationInfo", {}).get("authToken", "")

    def get_grades_df(self):
        """
        Access all the grades for all the students
        :return: pd.DataFrame()
        """
        endpoint = "grades"
        response = requests.post(BASE_URL + endpoint, json={'courseId': COURSE_ID},
                                 headers={'authToken': self.auth_token, 'Content-Type': 'application/json'})
        response.raise_for_status()
        return make_df(response.json())

    def get_specific_grades_df(self, assignment: str):
        """
        Get all the grades for a given assignment
        :param assignment: str() of the name of the assignment.
        :return: pd.DataFrame() with name of assignment
        """
        df = self.get_grades_df()
        return df[df['assignmentTitle'] == assignment]

    def get_attendance(self):
        """
        Get the attendance of students for each session including non-academic
        :return: json of student attendance
        """
        endpoint = "attendance"
        response = requests.post(BASE_URL + endpoint, json={'courseId': COURSE_ID},
                                 headers={'authToken': self.auth_token, 'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()

    def get_today_attendance(self):
        """
        Gets the attendance for the most recent academic class session
        :return: pd.DataFrame() for today's class or the most academic class
        """
        today = ""
        for x in self.get_sessions()["calendarSessions"]:
            if datetime.date.fromisoformat(x["session"]["startTime"][:10]) == datetime.date.today() and x['session']['contextId'] == 1:
                today = x["session"]["name"]
                break
        return self.get_session_attendance_df(today)

    def get_attendance_df(self):
        """
        Get the attendance of students for each session including non-academic
        :return: pd.DataFrame() of student attendance
        """
        return make_df(self.get_attendance())

    def get_academic_attendance_df(self):
        """
        Get a dataframe of the academic sessions
        :return: pd.DataFrame() of only academic sessions.
        """
        attendance = self.get_attendance_df()
        attendance = attendance[~attendance['sessionName'].str.contains("not required", case=False)]
        return attendance

    def get_session_attendance_df(self, session: str):
        """
        Get the attendance of a given session
        :param session: str()
        :return: pd.DataFrame() where session name is provided
        """
        df = self.get_attendance_df()
        return df[df["sessionName"] == session]

    def get_sessions_list(self):
        """
        Get the name of all academic sessions
        :return: list() of str() for each academic session
        """
        sessions = []
        for x in self.get_sessions()["calendarSessions"]:
            if x["session"]["contextId"] == 1:
                sessions.append(x['session']['name'])
        return sessions

    def get_sessions(self):
        """
        Get all the sessions including non-academic
        :return: JSON of all the class sessions
        """
        endpoint = "sessions"
        response = requests.post(BASE_URL + endpoint, json={'enrollmentId': ENROLLMENT_ID},
                                 headers={'authToken': self.auth_token, 'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()

    def get_assignments(self):
        """
        Get all assignments for the course including non-academic
        :return: JSON of all the assignmetns in the course
        """
        endpoint = "assignments"
        response = requests.post(BASE_URL + endpoint, json={'enrollmentId': ENROLLMENT_ID},
                                 headers={'authToken': self.auth_token, 'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()

    def get_assignments_list(self):
        """
        Get the list of homework assignments for the boot camp
        :return: list() of the names of all HW assignments
        """
        assignments = []
        for x in self.get_assignments()["calendarAssignments"]:
            if x["contextId"] == 1:
                assignments.append(x['title'])
        return assignments

    def is_student_eligible_df(self):
        # todo: make a DF showing current # of absences and missed assignments
        """
        1. Student names
        2. Find the student's number of assignment submitted from the assignments that are currently avaliable
            Create a new method for this where you find the nearest assignment and all submissions
        3. Make df with columns: [Name, Absences, Missed Assignments, Eligibility]
        :return: pd.DataFrame() with columns: [Name, Absences, Missed Assignments, Eligibility]
        """
        None

    def get_current_grades_df(self):
        """
        Get all assignments that are due prior to today's date
        :return: pd.DataFrame() of all the assignments that are due prior to or inclusive of today's date
        """
        assignments = []
        for x in self.get_assignments()['calendarAssignments']:
            if x['required'] == 'true' and datetime.date.fromisoformat(x['dueDate'][:10]) <= datetime.date.today():
                assignments.append(x['title'])
        df = self.get_grades_df()
        return df.loc[df["assignmentTitle"].isin(assignments)]

    def get_absences_df(self):
        """
        Check all the classes prior to inclusive of today's date, check each name and get their absences
        :return: dict() of the name of the students and the total number of absences
        """
        sessions = []
        for x in self.get_sessions()["calendarSessions"]:
            if x['session']['contextId'] == 1 and datetime.date.fromisoformat(x['session']['startTime'][:10]) <= datetime.date.today():
                sessions.append(x["session"]['name'])

        df = self.get_academic_attendance_df()
        df = df.loc[df["sessionName"].isin(sessions)]
        df = df.fillna(value=False)

        names = list(df["studentName"].unique())
        absences = []
        for x in names:
            temp_df = df.loc[df["studentName"] == x]
            absences.append(len(temp_df.loc[temp_df['present'] == False]))

        return pd.DataFrame(
            {
                "name": names,
                "absences": absences
            }
        )



    @staticmethod
    def get_present_students_dict(df: pd.DataFrame):
        """
        Taking a data frame return all the students that are checked in and absent in today's class as of that instance of calling the API
        :param df: pd.DataFrame() you get from BootCampSpot.get_today_attendance()
        :return: dict() of students checked into class. [present] | [absent]
        """
        return dict(
            {
                'present': df.loc[df["present"] == True]['studentName'].tolist(),
                'absent': df.loc[df["present"] == False]['studentName'].tolist()
            }
        )

    @staticmethod
    def get_next_homework_submission_dict(df: pd.DataFrame):
        """
        Take the grades data frome and locate who has submitted the assignment.
        :param df: pd.DataFrame() you get from BCS.get_specific_grades_df()
        :return: dict() of students name on homework submission status. [submitted] | [not_submitted]
        """
        return dict(
            {
                'submitted': df.loc[df['submitted'] == True]['studentName'].tolist(),
                'not_submitted': df.loc[df['submitted'] == False]['studentName'].tolist()
            }
        )
