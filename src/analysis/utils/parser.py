# parser.py - Special parser for reading and writing *.tsv files with pandas.

# Import pandas library for parsing dataframes.
import pandas as pd

# For parsing MFI tables specifically.
def read_mfi(path, title="Metric", countries=['AFG', 'JPN']):
    """Special parser for reading an MFI table.

    :param path: Path to the table to parse.
    :param title: fieldname to assign the value column, defaults to 'Metric'    
    """
    # Parse the MFI table.
    df = read_tsv(path)

    # Rename the columns.
    df.columns = [ "Code", "Country", "Year", title ]

    # Select only the entries that have matching codes.
    df = df[df["Code"].isin(countries)]
    
    # Replace 'Year' column with DataTime type values.
    df['Year'] = pd.to_datetime(df['Year'], format="%Y")
    
    # Create a MultiIndex in the pd.DataFrame.
    df = df.set_index(['Code', 'Year'], drop=True)
        
    # Sort by country and year.
    df = df.sort_index(ascending=True)

    # Return the table.
    return df

def read_tsv(filepath_or_buffer, **kwargs):
    """Read a tab-separated values (tsv) file into DataFrame.

    :param filepath_or_buffer: Any valid string path is acceptable. The string could be a URL.
    :param **kwargs: See expected keyword arguments for pandas.read_csv()
    :return: DataFrame or TextParser : Parsed file is returned as two-dimensional data structure with labeled axes.
    """
    return pd.read_csv(filepath_or_buffer, **dict(kwargs, sep="\t"))


def to_tsv(data, *args, **kwargs):
    """Write object to a tab-separated values (tsv) file.

    :param data: Data to write.
    :param *args: See expected positional arguments for pandas.to_csv()
    :param **kwargs: See expected keyword arguments for pandas.to_csv()
    :return: None or str : If path_or_buf is None, returns the resulting tsv format as a string. Otherwise returns None.
    """
    if isinstance(data, pd.DataFrame):
        _data = data
    elif isinstance(data, pd.Series):
        _data = data.to_frame()
    else:
        _data = pd.DataFrame(data)

    return _data.to_csv(*args, **dict(kwargs, sep="\t"))
