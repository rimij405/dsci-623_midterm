# analyser.py - Contains functions for summarizing datasets in analysis.ipynb

# Import project custom modules and Classes.
from ..utils import validate

# Import standard library for parsing aids.
from enum import Enum

# Import third-party libraries.
import numpy as np
import pandas as pd


class QueryMode(Enum):
    """QueryMode, subclass of Enum.
    
    :return: ALL, query pd.DataFrame for matching against all results.
    :return: ANY, query pd.DataFrame for matching against any result.
    """    
    ANY = 0
    ALL = 1


def find_in(df, find, mode=QueryMode.ANY, axis=1):    
    """Find exact match of value anywhere in the pd.DataFrame.

    :param df: pd.DataFrame containing dataset to query.
    :param find: int, str, or float containing the value to find. int and str are NOT interchangeable.
    :param mode: determines use of .any and .all methods, defaults to QueryMode.ANY
    :param axis: determines axis to apply search along, defaults to 1
    :return: If results are found, returns pd.DataFrame or pd.Series containing the results.
    """  
    results = None
    if len(df.index) > 0:
        if mode == QueryMode.ANY:
            results = df[df.isin([find]).any(axis)]
        elif mode == QueryMode.ALL:
            results = df[df.isin([find]).all(axis)]
           
    # print(f'Found {len(results.index)} result(s) for search term: {find}')
    
    if len(results.index) == 0 and validate.is_numeric(find):        
        if mode == QueryMode.ANY:
            numeric_results = df[df.isin([int(find)]).any(axis)]
        elif mode == QueryMode.ALL:
            numeric_results = df[df.isin([int(find)]).all(axis)]        
        if len(numeric_results.index) > 0:
            print(f'Warning: Found {len(numeric_results.index)} result(s) for numeric search: {int(find)}. Check if search must be fixed.')
            
    # Will return nothing if query mode is invalid.
    return results


def find_intersection(*args):
    """Find intersecting list of values between an arbitrary number of arguments.

    :return: Returns list[] containing intersecting values.
    """    
        
    # Original case:
    # unique_codes = list(country_codes['ped'].intersection(country_codes['gtd'].intersection(country_codes['mfi'])))

    # No args, no intersection.
    if args is None:
        return None
    
    # If there are args, incrementally find the intersection among all of them.
    if len(args) > 0:
        set_values = set(args[0])
        for i in range(len(args)):
            set_values = set_values.intersection(set(args[i]))
        return list(set_values)
    
    # If not returned, return nothing.
    return None


def percentile(n):
    """Calculate the quartile value for the given percentile.

    :param n: Percentile to find.
    :return: Returns function for use in pd.DataFrame.agg() calls.
    """    
    
    def _percentile(x):
        return x.quantile(n)
    _percentile.__name__ = "{:2.0f}%".format(n*100)
    return _percentile


def IQR():        
    """Calculate the inter-quartile range. (IQR = Q3 - Q2)

    :return: Returns function for use in pd.DataFrame.agg() calls.
    """    
    
    def _IQR(x):
        Q1 = percentile(0.25)(x)
        Q3 = percentile(0.75)(x)
        return Q3 - Q1
    _IQR.__name__ = "IQR"
    return _IQR


def spread():
    """Calculate the range between the minimum and maximum values. (spread = max - min).
    
    :return: Returns function for use in pd.DataFrame.agg() calls.
    """    
    
    def _spread(x):
        _min = x.min()
        _max = x.max()
        return _max - _min
    _spread.__name__ = "range"
    return _spread


def agg(df, target, fns):
    """Describe common aggregate statistics regarding the MFI dataset.

    :param mfi_df: pd.DataFrame containing MFI data to describe.
    :param target: str to aggregate data for.
    :param fns: list[str or fns], aggregate functions to run.
    :return: Returns pd.DataFrame containing description statistics.
    """    
    try:
        return df.agg({
            target: fns
        })
    except (KeyError, TypeError) as e:
        print(e)
        pass
    
    print(type(df))

    if isinstance(df, pd.core.groupby.DataFrameGroupBy):
        target = df.obj.columns.values[int(target)]
    elif isinstance(df, pd.DataFrame):
        target = df.columns.values[int(target)]
    return df.agg({
        target: fns
    })
    

def describe_numeric(df, target=1, fns=[
    'count',
    'mean',
    'std',
    'var',
    'min',
    'max',
    spread(),
    percentile(0.0),
    percentile(0.25),
    percentile(0.75),
    percentile(1.0),
    IQR()
]):
    """Custom description functions that adds extra fields by default (compared to pd.DataFrame.describe())

    :param mfi_df: pd.DataFrame containing MFI data to describe.
    :param target: column to target, defaults to 1
    :param fns: list[str or fn] containing aggregate functions to describe, defaults to [ 'count', 'mean', 'std', 'var', 'min', 'max', spread(), percentile(0.0), percentile(0.25), percentile(0.75), percentile(1.0), IQR() ]
    :return: Return pd.DataFrame containing aggregated description statistics.
    """    
    
    # Initial Case.
    # mortality_df.groupby(['Code']).agg({
    #    'Mortality Rate': ['count', 'mean', 'std', 'min', 'max', range_(), percentile(0), percentile(.25), percentile(.5), percentile(.75), percentile(1), IQR() ]
    # })
    
    return agg(df, target, fns)
    
    