import base64
import os
from datetime import datetime, timedelta, time
from dateutil.parser import parse
from dateutil import tz


CURRENT_TIME = "2023-01-25 18:13:22.47922 UTC"
LOCAL_TIME_START = "00:00:00"
LOCAL_TIME_END = "23:59:59"


def get_time_of_x_days_before(current_time, days):
    format_str = '%Y-%m-%d %H:%M:%S.%f %Z'
    given_time = parse(current_time)

    x_days_ago = given_time - timedelta(days=days)

    return x_days_ago.strftime(format_str)

def generate_report_id():
    random_bytes = os.urandom(6)
    report_id = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode('ascii')
    return report_id

def convert_utc_to_local(utc_time, timezone):
    try:
        tz_target = tz.gettz(timezone)
    except tz.UnknownTimeZoneError as err:
        # Handle timezone loading errors
        return "", ""

    local_time = utc_time.astimezone(tz_target)

    day = local_time.strftime("%A")

    return local_time.strftime("%H:%M:%S"), day

def convert_utc_str_to_local(utc_timestamp, timezone_str):
    utc_time = parse(utc_timestamp)

    tz_target = tz.gettz(timezone_str)

    local_time = utc_time.astimezone(tz_target)

    day_of_week = local_time.strftime("%A")

    return local_time, day_of_week

def get_day_mapping(day):
    if day == "Monday":
        return 0
    elif day == "Tuesday":
        return 1
    elif day == "Wednesday":
        return 2
    elif day == "Thursday":
        return 3
    elif day == "Friday":
        return 4
    elif day == "Saturday":
        return 5
    elif day == "Sunday":
        return 6
    else:
        return -1

def check_time_lies_between_two_time(start_time_str, end_time_str, local_time_str, timezone):
    loc = tz.gettz(timezone)

    # Parse the start, end, and local time
    start_time = parse(start_time_str).astimezone(loc)
    end_time = parse(end_time_str).astimezone(loc)
    local_time = parse(local_time_str).astimezone(loc)

    local_hour, local_minute, local_second = local_time.hour, local_time.minute, local_time.second
    start_hour, start_minute, start_second = start_time.hour, start_time.minute, start_time.second
    end_hour, end_minute, end_second = end_time.hour, end_time.minute, end_time.second

    if (local_hour >= start_hour and local_hour <= end_hour and
        ((local_hour > start_hour or (local_hour == start_hour and local_minute >= start_minute and local_second >= start_second)) and
         (local_hour < end_hour or (local_hour == end_hour and local_minute <= end_minute and local_second <= end_second)))):
        return True
    return False


def get_chunk_number_from_end(end_time_str, input_time_str):
    try:
        input_time = parse(input_time_str)
        end_time = parse(end_time_str)
        minutes = int((end_time - input_time).total_seconds() / 60)
        chunk = minutes // 60
        return chunk
    except ValueError:
        return -1