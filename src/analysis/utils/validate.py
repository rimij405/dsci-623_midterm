# validate.py - Contains validation checks.


def is_empty(s):
    """Check if input string or iterable is empty.  
      
    :param s: String or iterable to check.
    :return: True if input is empty.
    """
    if s:
        return False
    else:
        return True


def is_whitespace(s):
    """Check if input string is empty or contains only whitespace.
    
    :param s: String to check.
    :return: True if input is only whitespace.
    """
    return is_empty("".join(s.strip()))


def is_numeric(s):
    """Check if input string is a numeric.
    
    :param s: String to check.
    :return: True if input is a numeric. False if empty or not a numeric.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False
