import re


def validate_time(value):
    pattern = re.compile(r"^\d+\d(:[0-5]\d(\.\d+))$")
    return pattern.match(value) is not None


def validate_offset(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
