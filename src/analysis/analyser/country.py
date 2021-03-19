# country.py - Contains logic for Country key representations.

# print(f"Imported {__name__} country.py")

# Import utilities for initializing the analyzer.
from ..utils import validate
from ..utils import formatter
from ..analyser import analyser

# Import standard libraries.
from enum import Enum

# Import scikit libraries.
import pandas as pd

# Map of human readable type name to actual value.
class IDType(Enum):
    ID = 0
    CODE = 1
    LABEL = 2

# Instance of a country key.
class Country:
    """
    Representation of a country key.
    """
    
    ##################
    # Static Methods #
    ##################

    @classmethod
    def format(cls, country, layout='{}', sep=None):
        """Given Country or iterable[Country], give the formatted list[str] for each (or str, if one).

        :param country: iterable[Country] or Country, to be formatted.
        :param layout: str, the format one Country should be printed with, defaults to '{}'
        :param sep: str, the delimeter for joining, defaults to None.
        :raise ValueError: Raises ValueError if layout passed is invalid.
        :return: list[str] or str, containing necessary information. Returns the default layout if no Country data is shown.
        """        
        if country is None:
            return formatter.format_obj(None, layout)
                    
        return formatter.format_obj(country, layout, sep)
    
    @classmethod
    def get_countries(cls, countries_df):
        """Convert pd.DataFrame containing Country information into Country objects.

        :param countries_df: Country pd.DataFrame.
        """    
        # If invalid schema, raise error.
        if countries_df is None or not isinstance(countries_df, (pd.DataFrame, pd.Series)):
            raise ValueError(f"Cannot parse object of type {type(countries_df)}.")        
        
        # If series, convert.
        if isinstance(countries_df, pd.Series):
            return Country.from_series(countries_df) 
            
        else:      
            # If invalid schema, raise error.
            if not {'ID', 'Code', 'Country'}.issubset(countries_df.columns):
                raise ValueError("pd.DataFrame has invalid schema.")
            
            # If empty, but correct schema, return None.
            if len(countries_df.index) == 0:
                return None

            # If not empty, has correct schema, return list of Country objects.
            return Country.from_frame(countries_df)               
        
    ################
    # Constructors #
    ################

    def __init__(self, id_=None, code=None, label=None):
        """Initialize instance of Country, with optional identifiers.

        :param id_: Country ID, defaults to None
        :param code: Country Code, defaults to None
        :param name_: Country Name, defaults to None
        """
        if isinstance(id_, Country):
            self._identifier = id_._identifier
            return        
        
        self._identifier = {
            IDType.ID: None,
            IDType.CODE: None,
            IDType.LABEL: None,
        }

        try:
            self.id_ = id_
        except ValueError:
            pass

        try:
            self.code = code
        except ValueError:
            pass
        
        try:
            self.label = label
        except ValueError:
            pass

    @classmethod
    def from_frame(cls, df_, search=None, index=None):
        """Select one entry from the 2d table and fill construct instance using it.

        :param df: pd.DataFrame containing at least one entry.
        :param index: Index or search query to find entry, defaults to 0.
        :returns: list[Country] or Country, of instances described by the input data.
        """        
        # Only process constructor if we received a non-empty pd.Series or pd.DataFrame.
        if len(df_.index) > 0 and isinstance(df_, pd.DataFrame):  
                                        
            # Rename the columns for streamlined searches.
            df = df_.set_axis(['ID', 'Code', 'Country'], axis=1, inplace=False)
            
            # If search is not provided and index is not provided, process all items in the dataframe.
            if search is None and index is None:
                
                # Return each instance created by every row (and all columns) in the entire dataset.
                # Otherwise, return None.
                results = df_.loc[:,:].values
                if len(results) == 0:
                    return None
                else:
                    return [cls(*row) for row in results]
                
            # If search is not provided, but index is valid, process all items in the dataframe.
            if search is None and validate.is_numeric(index):
                
                # Return an instance for the specific index, if it exists.
                # Otherwise, return None.
                result = df_.iloc[index,:].values
                if len(result.index) == 0:
                    return None
                else:
                    return cls(*result)
                
            # If search is provided and search is an iterable, process each item individually.
            if search is not None:
                
                def find_all(terms):
                    results = list(map(lambda x: analyser.find_in(df, x), terms))
                    results = list(filter(lambda x: len(x.index) != 0, results))
                    print(f'Found {len(results)} result(s) for search terms: {", ".join([str(term) for term in terms])}')
                    if len(results) == 0:
                        return None
                    return results
                    
                def find(term):
                    result = analyser.find_in(df, term)
                    if len(result.index) == 0:
                        return None
                    return result
                
                # Try as an iterable first.
                try:
                    if isinstance(search, str):
                        raise TypeError(f"Single string '{search}' should not be treated as iterable in this instance.")
                    results = find_all(search)
                    if results is not None and len(results) >= 1:
                        return [cls(*(result.iloc[0,:].array)) for result in results]                    
                    return None
                except TypeError as e:
                    # Search is not an iterable.
                    # raise e
                    # print(f'`{search}` is not an iterable. {e}.')
                    pass
                
                result = find(search)
                if result is not None and len(result.index) >= 1:
                    return cls(*(result.iloc[0,:].array))
                return None
                                
        # Failed to create class.
        return ValueError("No pd.DataFrame provided to create class from.")
    
    @classmethod
    def from_series(cls, series):
        """Construct Country from pd.Series instance.

        :param series: pd.Series, contains Country data.
        :return: Country
        """        
        if series is not None and len(series.index) > 0:
            return cls(series[0], series[1], series[2])
        else:
            return cls()
        
    @classmethod
    def from_dict(cls, dict_):
        """Construct Country from dict instance.

        :param dict_: dict, contains Country data with keys "ID", "Code", and "Country".
        :return: Country
        """        
        if dict_ and len(dict_) > 0:
            return cls(dict_["ID"], dict_["Code"], dict_["Country"])
        else:
            return cls()

    @classmethod   
    def from_tuple(cls, tuple_):        
        """Construct Country from tuple instance.
        
        :param tuple_: tuple, contains Country data in form of (id_, code, label)
        :return: Country
        """     
        if tuple_:
            # id_, code, label = tuple_
            return cls(*tuple_)
        else:
            return cls()

    @classmethod
    def from_list(cls, list_):
        """Construct Country from list instance.

        :param list_: list, contains Country data in form of [id_, code, label]
        :return: Country
        """     
        if list_ and len(list_) > 0:
            # id_, code, label = list_
            return cls(*list_)
        else:
            return cls()

    def __repr__(self):
        """Returns a machine-readable string representing the object.

        :return: string, machine-readable.
        """
        return f'Country(id_={self.id_}, code={self.code}, label={self.label})'

    def __str__(self):
        """Returns a human-readable string describing the object.

        :return: string, display or discription of the object.
        """
        return f'<[{self.code} {self.id_}]: "{self.label}">'

    @classmethod
    def is_valid(cls, instance):
        if instance is None:
            return False
        
        if not isinstance(instance, cls):
            return False

        if instance.id_ is None or instance.code is None:
            return False    
        
    ##############
    # Properties #
    ##############

    @property
    def identifier(self):
        """Property representing dictionary of identifiers.
        
        :return: dict containing self.id_, self.code, and self.label values.
        """
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        """Set the identifiers using a dict.

        :param value: dict containing the identifier values.
        """
        # Copy existing dict.
        fallback = dict(self._identifier)

        # Attempt to access like array, tuple or dict.
        try:
            # Ensure all identifiers are callable. Will fail if any is not.
            data = (value[IDType.ID], value[IDType.CODE], value[IDType.LABEL])

            # Assign via properties.
            self.id_ = data[IDType.ID]
            self.code = data[IDType.CODE]
            self.label = data[IDType.LABEL]

            # No errors raised, so we can delete our fallback gracefully.
            del fallback
        except (AttributeError, TypeError, LookupError):
            # Rollback changes.
            self._identifier = fallback
            raise ValueError(
                "Input identifier format unrecognized. Cannot assign identifiers."
            )

    @identifier.deleter
    def identifier(self):
        """
        Property deleter for self.identifier.
        """
        del self.id_
        del self.code
        del self.label

    @property
    def id_(self):
        """Property representing numeric id assigned to this country in the Global Terrorism Database.

        :return: string cast numeric id.
        """
        return self._identifier[IDType.ID]

    @id_.setter
    def id_(self, value):
        """
        Property setter for self.id_.

        :param value: numeric id
        """
        if self._get_identifier_type(value) != IDType.ID:
            raise ValueError("Identifier is not a numeric ID.")
        else:
            self._identifier[IDType.ID] = value

    @id_.deleter
    def id_(self):
        """
        Property deleter for self.id_.
        """
        self._identifier[IDType.ID] = None

    @property
    def code(self):
        """Property representing the three-letter country code assigned to this country in the MFI and PED datasets.

        :return: string representing three-letter code.
        """
        return self._identifier[IDType.CODE]

    @code.setter
    def code(self, value):
        """
        Property setter for self.code.

        :param value: three-letter string.
        """
        if value is None or self._get_identifier_type(value) != IDType.CODE:
            raise ValueError("Identifier is not a three-letter code.")
        else:
            self._identifier[IDType.CODE] = value

    @code.deleter
    def code(self):
        """
        Property deleter for self.code.
        """
        self._identifier[IDType.CODE] = None

    @property
    def label(self):
        """Property representing the human-readable name assigned to this country in the MFI dataset.

        :return: string representing the human-readable name.
        """
        return self._identifier[IDType.LABEL]

    @label.setter
    def label(self, value):
        """
        Property setter for self.label.

        :param value: any string.
        """
        if value is None or self._get_identifier_type(value) != IDType.LABEL:
            raise ValueError("Identifier is not a label.")
        else:
            self._identifier[IDType.LABEL] = value

    @label.deleter
    def label(self):
        """
        Property deleter for self.label.
        """
        self._identifier[IDType.LABEL] = None

    def set_identifier(self, identifier, identifier_type):
        """Set the appropriate identifier value based on infered details, so long as it matches the explicit type.
        
        :param identifier: Identifier value to assign.
        :param identifier_type: IDType enum to ensure value matches before assigning.
        :raises ValueError: Error raised when no identifier value or valid type is provided.
        """

        # If no arguments provided, exit.
        if (
            identifier is None
            and identifier_type is None
            and identifier_type not in [e.values for e in IDType]
        ):
            raise ValueError("Cannot assign field with no arguments provided.")

        # Assign the validation type.
        id_type = self._get_identifier_type(identifier)
        validation_type = identifier_type

        # If identifier type is not provided, but we have input, infer the identifier type.
        if identifier and validation_type is None:
            validation_type = id_type

        # If the identifier type matches the validation type, assign it.
        if id_type and id_type == validation_type:
            self._identifier[id_type] = identifier

    ###################
    # Service Methods #
    ###################   
        
    def eq(self, other):     
        if not Country.is_valid(other) or not Country.is_valid(self):
            return False
        
        # Labels can be mismatched.
        # Now return comparison between the keys, the id and code. They must match exactly.
        return self.id_ == other.id_ and self.code == other.code
        
    def el(self, other):
        if not Country.is_valid(other) or not Country.is_valid(self):
            return False

        return self.id_ <= other.id_

    def eg(self, other):
        if not Country.is_valid(other) or not Country.is_valid(self):
            return False

        return self.id_ >= other.id_ 
    
    def lt(self, other):
        if not Country.is_valid(other) or not Country.is_valid(self):
            return False

        return self.id_ < other.id_

    def gt(self, other):
        if not Country.is_valid(other) or not Country.is_valid(self):
            return False

        return self.id_ > other.id_ 
        
    def to_frame(self, *args, **kwargs):
        """Export instance values as a DataFrame.
        
        :returns: pd.DataFrame, containing instance information.
        """
        return pd.DataFrame.from_dict(self.to_dict(), *args, **kwargs)
    
    def to_series(self, *args, **kwargs):
        """Export instance values as a Series.
        
        :returns: pd.Series, containing instance information.
        """
        return pd.Series(self.to_dict(), *args, **kwargs)
    
    def to_dict(self):
        """Export instance values as a dict.
        
        :returns: dict, containing instance information.
        """
        return {
            "ID": self.id_,
            "Code": self.code,
            "Country": self.label
            }
        
    def to_tuple(self):
        """Export instance values as a tuple.
        
        :returns: tuple, containing instance information.
        """
        return (self.id_, self.code, self.label)
    
    def to_list(self):
        """Export instance values as a list.
        
        :returns: list, containing instance information.
        """
        return [self.id_, self.code, self.label]
    
    ###################
    # Private Methods #
    ###################
        
    def _get_identifier_type(self, identifier):
        """Get country identifier type for flexible assignment purposes.

        :param identifier: Identifier value representing a country ID, code, or name.        
        :return: Return None if no value is provided or if it's not a valid value. Else, return appropriate type.
        """

        # No type if nothing provided.
        if identifier is None:
            return None

        # If identifier is numeric, it's an id number.
        if validate.is_numeric(identifier):
            return IDType.ID

        # If it's a non-empty string, it's either a name or code.
        if isinstance(identifier, str) and not validate.is_empty(identifier):
            if len(identifier) == 3:
                return IDType.CODE
            else:
                return IDType.LABEL

        # If nothing caught, return None. 
        return None