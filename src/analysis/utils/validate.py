# validate.py - Contains validation checks.

# Import standard library helpers.
import unicodedata

def normalize_nfkd(s):
    """Perform NFKD normalization on an input string.

    :param s: String to normalize.
    :return: Returns normalized string.
    """    
    return unicodedata.normalize("NFKD", s)


def caseless_compare(a, b):
    """Given two strings, perform a caseless comparison between them.

    :param a: Left-hand string.
    :param b: Right-hand string.
    :returns: Returns 0 if equal. Returns 1 if the normalized a > b, alphabetically. Otherwise, returns -1.
    """    
    if a is None or b is None:
        raise ValueError("Cannot compare to None-type argument.")
    
    # Will fail if either is not a string.
    norm_a = normalize_nfkd(a.casefold())
    norm_b = normalize_nfkd(b.casefold())
    
    if norm_a == norm_b:
        return 0
    elif norm_a > norm_b:
        return 1
    elif norm_a < norm_b:
        return -1


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
    except (TypeError, ValueError):
        return False
