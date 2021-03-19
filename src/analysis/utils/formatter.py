# formatter.py - Helper functions for analysis.

def format_obj(obj, layout='{}', sep=None):
    """Given an obj or dict[obj] and a format, returns formatted strings.

    :param obj: iterable[obj] or obj, containing info to print.
    :param layout: str, the format one object should be printed with, defaults to '{}'
    :param sep: str, the delimeter for joining, defaults to None.
    :raise ValueError: Raises ValueError if layout passed is invalid.
    :return: list[str] or str, containing necessary information. Returns the default layout if no object is passed.
    """    
    # If layout is None, default to '{}'
    if layout is None or not isinstance(layout, str):
        raise ValueError("Cannot print object without formatted string.")
        
    # If object is None, return the layout without any preprocessing.
    if obj is None:
        return layout

    def format_item(item):        
        return layout.format(item)
    
    def format_iterable(list_obj):        
        return [format_item(item) for item in list_obj]    
    
    try:
        results = format_iterable(obj)
        if len(results) == 0:
            return layout
        
        if sep is None:
            return results
        else:
            return sep.join(results)
    except TypeError as e:
        print(f'`{obj}` is not an iterable. Formatting single item.')
        pass

    return format_item(obj)