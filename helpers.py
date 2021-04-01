import json
from datetime import datetime


def parse_time_string(time):
    return datetime.fromisoformat(time[:-1])


def read_json_file(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)
