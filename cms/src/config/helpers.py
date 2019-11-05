def to_boolean(value):
    """Returns a boolean value parsed from most common thruthy env variables."""
    if value is None:
        return False

    if value in ('True', 'true', 't', '1', 1, True):
        return True

    return False
