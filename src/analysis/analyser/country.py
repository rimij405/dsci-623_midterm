# country.py - Contains logic for Country key representations.

# print(f"Imported {__name__} country.py")

# Import utilities for initializing the analyzer.
from ..utils import validate

# Import standard libraries.
from enum import Enum

# Import scikit libraries.
# import numpy as np
# import pandas as pd

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

    ################
    # Constructors #
    ################

    def __init__(self, id_=None, code=None, label=None):
        """Initialize instance of Country, with optional identifiers.

        :param id_: Country ID, defaults to None
        :param code: Country Code, defaults to None
        :param name_: Country Name, defaults to None
        """
        self._identifier = {
            IDType.ID: None,
            IDType.CODE: None,
            IDType.LABEL: None,
        }

        if id_:
            self.id_ = id_

        if code:
            self.code = code

        if label:
            self.label = label

    @classmethod
    def from_frame(cls, df, index=0, search=None):
        """Select one entry from the 2d table and fill construct instance using it.

        :param df: pd.DataFrame containing at least one entry.
        :param index: Index or search query to find entry, defaults to 0.
        """
        # If we have data...
        if df and len(df.index) > 0 and len(df.columns) >= 3:
            arr = None

            # If search is provided, it takes precedence.
            if search and not validate.is_empty(search):
                if search in df["Country"].values:
                    arr = df[df["Country"] == search].iloc[index, :].array
                elif search in df["Code"].values:
                    arr = df[df["Code"] == search].iloc[index, :].array
                elif validate.is_numeric(search):
                    if int(search) in df["ID"].values:
                        arr = df[df["ID"] == int(search)].iloc[index, :].array
            # If search was not provided, but index was...
            else:
                # If no index provided, we'll select the first row.
                if index is None:
                    index = 0
                else:
                    arr = df[["ID", "Code", "Country"]].iloc[index, :].array

            if arr and len(arr) >= 3:
                return cls(*arr)

        raise ValueError("No dataframe provided to construct Country() from.")

    @classmethod
    def from_series(cls, series):
        if series and len(series.index) > 0:
            return cls(series[0], series[1], series[2])
        else:
            return cls()

    @classmethod
    def from_tuple(cls, tuple_):
        if tuple_:
            # id_, code, label = tuple_
            return cls(*tuple_)
        else:
            return cls()

    @classmethod
    def from_list(cls, list_):
        if list_ and len(list_) > 0:
            # id_, code, label = list_
            return cls(*list_)
        else:
            return cls()

    def __str__(self):
        """Returns a string representing the object when cast as a string.

        :return: string, representing the object casted as a string.
        """
        return f'<[{self.code} {self.id_}]: "{self.label}">'

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
