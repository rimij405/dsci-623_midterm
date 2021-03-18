# parser.py - Special parser for reading and writing *.tsv files with pandas.

# Import pandas library.
import pandas as pd


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
