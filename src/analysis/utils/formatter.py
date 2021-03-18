# formatter.py - Helper functions for analysis.


def format_key(id, code=None, name=None):
    """Get key as formatted string.
    
    :param id: ID or entire composite key.
    :param code: Country code.
    :param name: Country plaintext name.
    :return: Return formatted string.
    """
    if code is None and name is None:
        id, code, name = id
    return f'< "{code}": ({id}) "{name}" >'


def format_keys(country_keys, *remaining_keys):
    """Get collection of several keys.

    :param keys: Single key or iterable containing several keys.
    :param remaining_keys: Remaining keys.
    :return: Return collection of formatted strings.
    """
    # Prepare collection for iteration.
    terms = []

    # If first argument is provided...
    if country_keys and len(country_keys) > 0:
        try:
            terms.extend(list(country_keys))
        except TypeError:
            # Ignore if not iterable.
            pass

    # Check if remaining_keys should be added.
    if remaining_keys and len(remaining_keys) > 0:
        try:
            terms.extend(list(remaining_keys))
        except TypeError:
            # Ignore if not iterable.
            pass

    # Return the formatted string for each.
    return "\n".join([f"{format_key(*term)}" for term in terms])
