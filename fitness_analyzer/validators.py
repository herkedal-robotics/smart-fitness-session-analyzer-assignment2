import re
from .exceptions import InvalidIdentifierError, InvalidRecordError

def validate_participant_id(participant_id):
    pattern = r"P\d{3}"
    # P = letter P,
    # \d = digit from 0 to 9
    # {3} = three of those digits

    if re.fullmatch(pattern,participant_id) is None:
        raise InvalidIdentifierError(
            f"Invalid participant ID: {participant_id}. Should be Pxxx."
        )
    return True

def validate_session_id(session_id):
    pattern = r"FIT-\d{4}-\d{3}"
    # FIT = letters F,I and T
    # \d = digits from 0 to 9
    # {3},{4} = either 3 or 4 of those digits

    if re.fullmatch(pattern,session_id) is None:
        raise InvalidIdentifierError(
            f"Invalid fitness session ID: {session_id}. Should be FIT-xxxx-xxx."
        )
    return True


# INITIALLY OUR PROGRAM CRASHES WHEN MEETS AN ERROR, BUT WE WILL
# FIX IT LATER ON
r"""
PS C:\Users\herke\ACIT4420\assignment2> python -c "from validators import validate_session_id; validate_session_id('FIT-26-102')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\herke\ACIT4420\assignment2\validators.py", line 24, in validate_session_id
    raise InvalidIdentifierError(
exceptions.InvalidIdentifierError: Invalid fitness session ID: FIT-26-102

"""

def validate_activity_level(activity_level):
    if activity_level < 0 or activity_level > 1:
        raise InvalidRecordError(
            f"Activity level must be between 0 and 1, but it is: {activity_level}"
        )
    return True

def validate_timestamp(timestamp):
    if timestamp < 0:
        raise InvalidRecordError(
            f"Timestamp can't be negative, but it is: {timestamp}"
        )
    return True

def validate_heart_rate(heart_rate):
    if heart_rate < 35 or heart_rate > 205:
        raise InvalidRecordError(
            f"Heart rate must be between 35 and 205, but it is: {heart_rate}"
        )
    return True

def validate_skin_response(skin_response):
    if skin_response < 0:
        raise InvalidRecordError(
            f"Skin response can't be negative, but it is: {skin_response}"
        )
    return True

def validate_temperature(temp):
    if temp < 25 or temp > 42:
        raise InvalidRecordError(
            f"Temperature must be between 25 and 42, but it is: {temp}"
        )
    return True

def validate_signal_quality(signal_quality):
    if signal_quality < 0 or signal_quality > 1:
        raise InvalidRecordError(
            f"Signal quality must be between 0 and 1, but it is: {signal_quality}"
        )
    return True
