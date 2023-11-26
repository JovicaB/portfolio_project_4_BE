from data.json_data_manager import JSONData
from datetime import datetime, timedelta

INTERVIEW_JSON = 'data/interview_data.json'


class DateManager:
    """
    A utility class for managing dates and day-related operations.

    Args:
        input_date (datetime): The input date used as a base for date calculations.

    Attributes:
        input_date (datetime): The input date provided when creating an instance.

    Methods:
        get_day_name(input_date):
            Retrieves the name of the day for a given date.

        english_to_serbian_day_name(day_name):
            Converts an English day name to Serbian.

        get_next_working_dates(days):
            Calculates and returns the next working dates.
    """

    def __init__(self) -> None:
        self.json_file = INTERVIEW_JSON
        self.json_data_encoder = JSONData(self.json_file)

    def get_interview_date(self):
        result = self.json_data_encoder.read_json(
            "interview_sessions")['session_date']
        date_object = datetime.strptime(result, "%d-%m-%Y")
        day = int(date_object.day)
        month = int(date_object.month)
        return [day, month]

    @staticmethod
    def get_day_name(day: int, month: int):
        """
        Retrieves the name of the day for a given date.

        Args:
            day (int): The day of the month.
            month (int): The month.

        Returns:
            str: The name of the day (e.g., "Monday").

        Example Usage:
            day_name = DateManager.get_day_name(3, 11)
        """
        current_year = datetime.now().year
        input_date = datetime(current_year, month, day)
        day_name = input_date.strftime('%A')
        return day_name

    @staticmethod
    def english_to_serbian_day_name(day_name: str):
        """
        Converts an English day name to Serbian.

        Args:
            day_name (str): The English day name to be converted.

        Returns:
            str: The Serbian day name or "Unknown" if not found in the mapping.

        Example Usage:
            english_day = "Monday"
            serbian_day = DateManager.english_to_serbian_day(english_day)
        """
        day_mapping = {
            "Monday": "Ponedeljak",
            "Tuesday": "Utorak",
            "Wednesday": "Sreda",
            "Thursday": "Četvrtak",
            "Friday": "Petak",
            "Saturday": "Subota",
            "Sunday": "Nedelja",
        }

        return day_mapping.get(day_name, "Unknown")

    @staticmethod
    def get_next_working_dates(day: int, month: int):
        """
        Calculates and returns the next x working dates.

        Args:
            days (int): The number of working days to calculate.

        Returns:
            dict: A dictionary with keys like "day_1", "day_2", and values as date JSON objects.

        Example Usage:
            input_date = datetime(2023, 11, 3)
            date_manager = DateManager(input_date)
            next_5_dates = date_manager.get_next_working_dates(5)
            print(next_5_dates)
        """
        current_year = datetime.now().year
        input_date = datetime(current_year, month, day)
        day_counter = 1

        result = []

        while len(result) < 7:
            input_date += timedelta(days=1)
            if input_date.weekday() < 5:
                key_date = f"day_{day_counter}"
                result.append([key_date, input_date.date().isoformat()])
                day_counter += 1

        return result

    @staticmethod
    def get_daily_schedules(start_time: str, end_time: str, session_duration: int, break_duration: int):
        start_time = datetime.strptime(start_time, "%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M")

        time_difference = (end_time - start_time).total_seconds() / 60

        total_session = session_duration + break_duration
        upper_bound = (time_difference // total_session)

        session = {}
        session_time = start_time

        i = 1
        while i <= upper_bound:
            key = session_time.time().isoformat()
            session[key] = {"name": None, "contact": None,
                            "city": None, "note": None}
            i += 1
            session_time += timedelta(minutes=total_session)
        return session


class Setup:
    def __init__(self) -> None:
        self.json_file = INTERVIEW_JSON
        self.json_data_encoder = JSONData(self.json_file)
        self.date_manager = DateManager()

    def is_basic_json_created(self):
        """
        Check if the basic JSON structure is created.

        Returns:
        bool: True if the basic structure exists, False otherwise.
        """
        try:
            basic_structure = self.json_data_encoder.read_json(
                "interview_sessions")
            return basic_structure is not None
        except Exception as e:
            print(f"Error checking basic JSON structure: {e}")
            return False

    def create_basic_json(self):
        """
        Create the basic JSON structure.

        Returns:
        str: A message indicating the success or failure of the operation.
        """
        basic_structure = self.json_data_encoder.read_json(
            "interview_sessions")
        if basic_structure is None:
            basic_structure = {}
            result = self.json_data_encoder.write_json(
                ["interview_sessions"], basic_structure)
            return result
        else:
            return "Basic JSON structure already exists."

    def is_interview_session_generated(self):
        try:
            basic_structure = self.json_data_encoder.read_json(
                "interview_sessions")
            return bool(basic_structure)
        except Exception as e:
            print(f"Error checking basic JSON structure: {e}")
            return False

    def generate_interview_session(self, input_data):

        session_title = input_data["project_name"]
        day = int(input_data["day"])
        month = int(input_data["month"])
        current_year = datetime.now().year
        session_date = str(day) + '-' + str(month) + '-' + str(current_year)

        english_day_name = self.date_manager.get_day_name(day, month)
        serbian_day_name = self.date_manager.english_to_serbian_day_name(
            english_day_name)

        start_time = input_data["start_time"]
        end_time = "16:00"
        session_duration = int(input_data["duration"])
        break_duration = int(input_data["break"])

        schedule_data = self.date_manager.get_daily_schedules(
            start_time, end_time, session_duration, break_duration)
        session_data = {
            "project name": session_title,
            "session_date": session_date,
            "day_name": [english_day_name, serbian_day_name],
            "days": {
                i[0]: {
                    "date": i[1],
                    "schedules": schedule_data
                } for i in self.date_manager.get_next_working_dates(day, month)
            }
        }

        self.json_data_encoder.write_to_interview_sessions(
            session_title, session_data)
        return f"JSON data created for interview session: {session_title}"


class InterviewSession:
    def __init__(self) -> None:
        self.json_file = INTERVIEW_JSON
        self.json_data_encoder = JSONData(self.json_file)
        self.main_key = "interview_sessions"

    def get_project_name(self):
        result = self.json_data_encoder.read_json(self.main_key)[
            'project name']
        return result

    def get_session_dates(self):
        session_data = self.json_data_encoder.read_json(self.main_key)

        interview_dates = []
        for day_key, day_value in session_data['days'].items():
            interview_dates.append(day_value['date'])

        return interview_dates

    def get_session_days(self):
        date_manager = DateManager()
        session_data = self.json_data_encoder.read_json(self.main_key)

        interview_days = {}
        interview_dates_eng = []
        interview_dates_sr = []
        for day_key, day_value in session_data['days'].items():
            date_str = day_value['date']
            date_proper = datetime.strptime(date_str, "%Y-%m-%d")
            day_number = date_proper.day
            month_number = date_proper.month
            day_str = date_manager.get_day_name(day_number, month_number)
            interview_dates_eng.append(day_str)
            interview_dates_sr.append(
                date_manager.english_to_serbian_day_name(day_str))

        interview_days['eng'] = interview_dates_eng
        interview_days['sr'] = interview_dates_sr

        return interview_days

    def get_free_schedules(self):
        session_data = self.json_data_encoder.read_json(self.main_key)

        free_schedules = []
        day_free_schedules = {}

        for day_key, day_value in session_data['days'].items():
            date = day_value['date']
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d-%m')

            for time, value in day_value['schedules'].items():
                if value['name'] is None:
                    time_obj = datetime.strptime(time, '%H:%M:%S')
                    formatted_time = time_obj.strftime('%H:%M')
                    free_schedules.append(formatted_time)

            day_free_schedules[formatted_date] = free_schedules
            free_schedules = []

        return day_free_schedules

    def get_interview_session_data(self):
        result = {
            'title': self.get_project_name(),
            'dates': self.get_session_dates(),
            'days': self.get_session_days(),
            'schedules': self.get_free_schedules()
        }

        return result

    def set_candidate(self, date, schedule, user_data):
        try:
            session_data = self.json_data_encoder.read_json(self.main_key)[
                'days']
            session_date_key = next(
                key for key, value in session_data.items() if value['date'] == date)
        except (KeyError, StopIteration):
            print("Error: Date not found in session data.")
            return

        keys_base = ["interview_sessions", "days",
                     session_date_key, "schedules", schedule]
        field_names = ["name", "contact", "city", "note"]

        for field_name, user_value in zip(field_names, user_data):
            keys = keys_base.copy()
            keys.append(field_name)
            try:
                self.json_data_encoder.write_json(keys, user_value)
            except IndexError:
                print(f"Error: Unable to write {field_name} to JSON data.")


class Report:
    def __init__(self) -> None:
        self.json_file = INTERVIEW_JSON
        self.json_data_encoder = JSONData(self.json_file)
        self.main_key = "interview_sessions"
    
    def get_report_data(self, lang:str='ENG'):
        """Get complete interview data from JSON

        Args:
            lang (str, optional): defaults is 'ENG'.

        Returns:
            dictionary with interview data 
        """
        raw_interview_data = self.json_data_encoder.read_json()
        title = raw_interview_data[self.main_key]['project name']
        interview_start_date = raw_interview_data[self.main_key]['session_date']
        interview_date_name = raw_interview_data[self.main_key]['day_name']

        if lang == 'ENG':
            interview_date_name = interview_date_name[0]
        elif lang == 'SR':
            interview_date_name = interview_date_name[1]

        interview_data = {
            'planner_data': [title, interview_start_date, interview_date_name],
            'days': []
        }

        schedules_data = raw_interview_data[self.main_key]['days']
        for days_data in schedules_data.values():
            daily_schedules = []
            for k, v in days_data['schedules'].items():
                schedule_info = [value for value in v.values() if value is not None and value[0] is not None] ############
                # schedule_info = [value for value in v.values() if value is not None and isinstance(value, list) and value and value[0] is not None]
                if schedule_info:
                    daily_schedules.append({k: schedule_info})

            interview_data['days'].append({days_data['date']: daily_schedules})

        return interview_data
