import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import List
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(levelname)s-%(message)s")


class HandlingStrategy(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame, features: List) -> pd.DataFrame:
        """Transforms the input DataFrame and returns the transformed DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: Transformed DataFrame.
        """
        pass


class Replace_infinte_values(HandlingStrategy):
    def transform(self, df: pd.DataFrame, features: List) -> pd.DataFrame:
        """Replaces infinte values with Nan values.

        Args:
            df (pd.DataFrame): Input Dataframe.
            features (List): List of features to be trasformed.

        Returns:
            pd.DataFrame : Transformed data.
        """
        df_cleaned = df.copy()
        df_cleaned.replace([np.inf, -np.inf], np.nan, inplace=True)
        logging.info(f"Infinte values replaced with Nan for features {features}.")
        
        return df_cleaned


class Filling_missing_values(HandlingStrategy):

    def __init__(self, method="mean", fill_values=None):
        """Initializes the specific method with which missing values are filled

        Args:
            method : Specific method with which data is filled
            fill_values : Specific value used to fill the missing value"""

        self.method = method
        self.fill_values = fill_values

    def transform(self, df: pd.DataFrame, features: List) -> pd.DataFrame:
        """Performs changes to the missing values

        Args:
            df (pd.DataFrame): Input DataFrame

        Returns:
            pd.DataFrame: Transformed DataFrame
        """
        df_cleaned = df.copy()

        for feature in features:
            if self.method == "mean":
                df_cleaned[feature] = df[feature].fillna(df[feature].mean())
            elif self.method == "median":
                df_cleaned[feature] = df[feature].fillna(df[feature].median())
            elif self.method == "mode":
                df_cleaned[feature] == df[feature].fillna(df[feature].mode())
            elif self.method == "constant":
                df_cleaned[feature] == df[feature].fillna(self.fill_values)
            else:
                logging.warning(f"Unknown methond '{self.method}'")

        logging.info("Missing values filled")

        return df_cleaned


class Handler:
    def __init__(self, strategy: HandlingStrategy):
        """Initializes the strategy for handling the data."""
        self._strategy = strategy

    def set_strategy(self, strategy: HandlingStrategy):
        """Sets the strategy for handling the data."""
        self._strategy = strategy

    def execute_strategy(self, df: pd.DataFrame, features: List):
        """Executes the strategy for handling the data."""
        self._strategy.transform(df, features)


if __name__ == "__main__":
    pass
