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


class ValidationError(Exception):
    def __init__(self, message="", *args, errors=None):
        self.errors = errors or []
        self.message = message or ("Validation Error:" + "\n" + "\n".join(self.errors))
        super().__init__(self.message, *args)

    def get_err_str(self):
        return "\n".join(self.errors)
