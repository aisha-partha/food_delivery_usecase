from typing import List
import sys
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder


class ColumnDropper(BaseEstimator, TransformerMixin):

    def __init__(self, col_list: list):

        if not isinstance(col_list, list):
            raise ValueError("Columns should be a list of strings")

        self.col_list = col_list

    def fit(self, dataframe = pd.DataFrame, target: pd.Series = None):

        return self

    def transform(self, dataframe = pd.DataFrame, target: pd.Series = None):

        df = dataframe.copy()
        df.drop(columns=self.col_list,inplace=True)

        return df
    
class Binner(BaseEstimator, TransformerMixin):
    
    def __init__(self, col_list:list, bins:list, labels:list):

        if not isinstance(col_list, list):
            raise ValueError("Columns should be a list of strings")
            
        if not isinstance(bins, list):
            raise ValueError("Bins should be a list of integers")

        if not isinstance(labels, list):
            raise ValueError("Bins should be a list of strings")
        
        if bins is not None and labels is not None and len(bins) != len(labels) + 1:
            raise ValueError("Length of bins must be one more than the length of labels.")
            
        self.col_list = col_list
        self.bins = bins
        self.labels = labels        
    
    def fit(self, dataframe: pd.DataFrame, target: pd.Series = None):

        return self
    
    def transform(self, dataframe: pd.DataFrame):
        df =  dataframe.copy()
        
        for col in self.col_list:
            df[f"{col}_binned"] = pd.cut(df[col], bins=self.bins, labels=self.labels, right=False)
            
        return df
    

class Mapper(BaseEstimator, TransformerMixin):
    """
    Ordinal categorical variable mapper:
    Treat column as Ordinal categorical variable, and assign values accordingly
    """

    def __init__(self, col_map: dict):

        if not isinstance(col_map, dict):
            raise ValueError("Mappings should be a dictionary of col, strings pair")
        self.col_map = col_map

    def fit(self, dataframe: pd.DataFrame, target: pd.Series = None):

        return self

    def transform(self, dataframe: pd.DataFrame):
        
        df = dataframe.copy()

        for key, val in self.col_map.items():
            df[key] = df[key].map(val)

        return df
    
    
class OutlierHandler(BaseEstimator, TransformerMixin):
    """
    Change the outlier values:
        - to upper-bound, if the value is higher than upper-bound, or
        - to lower-bound, if the value is lower than lower-bound respectively.
    """

    def __init__(self, col_list: list):

        if not isinstance(col_list, list):
            raise ValueError("Columns should be a list of strings")
        self.col_list = col_list
        self.limit_dict = {}

    def fit(self, dataframe: pd.DataFrame, target: pd.Series = None):

        df = dataframe.copy()
        # limit_dict = {}

        for col in self.col_list:

            q1 = df.describe()[col].loc['25%']
            q3 = df.describe()[col].loc['75%']
            iqr = q3 - q1
            lower_bound = int(q1 - (1.5 * iqr))
            upper_bound = int(q3 + (1.5 * iqr))
            self.limit_dict[col] = [lower_bound, upper_bound]

        self.limits = self.limit_dict
        return self


    def transform(self, dataframe: pd.DataFrame):
        
        df = dataframe.copy()

        for col in self.col_list:
            for i in df.index:

                if df.loc[i,col] > self.limits[col][1]:
                    df.loc[i,col]= self.limits[col][1]

                if df.loc[i,col] < self.limits[col][0]:
                    df.loc[i,col]= self.limits[col][0]

        return df
    

class ColOneHotEncoder(BaseEstimator, TransformerMixin):
    """ One-hot encode a column """

    def __init__(self, col_list: list):

        if not isinstance(col_list, list):
            raise ValueError("Columns should be a list of strings")

        self.col_list = col_list
        self.categories_ = {}

    def fit(self, dataframe: pd.DataFrame, target: pd.Series = None):

        df = dataframe.copy()
        for col in self.col_list:
            self.categories_[col] = df[col].unique()
            self.categories_[col] = [col for col in self.categories_[col] if str(col) != 'nan']

        return self

    def transform(self, dataframe: pd.DataFrame):
        
        if not self.categories_:
            raise ValueError("Must fit the transformer before transforming the data.")

        df = dataframe.copy()
        for col in self.col_list:
            categories = self.categories_[col]
            for category in categories:
                new_column_name = f"{col}_{category}"
                df[new_column_name] = (df[col] == category).astype(int)
            df = df.drop(col, axis=1)

        return df

class ColLabelEncoder(BaseEstimator, TransformerMixin):
    """ One-hot encode a column """

    def __init__(self, col_list: list):

        if not isinstance(col_list, list):
            raise ValueError("Columns should be a list of strings")

        self.col_list = col_list
        self.encoders = {}

    def fit(self, dataframe: pd.DataFrame, target: pd.Series = None):

        df = dataframe.copy()
        for column in self.col_list:
            
            le = LabelEncoder()
            le.fit(df[column])
            self.encoders[column] = le
            
        return self

    def transform(self, dataframe: pd.DataFrame):
        
        if not self.encoders:
            raise ValueError("Must fit the transformer before transforming the data.")

        df = dataframe.copy()

        for column, le in self.encoders.items():
            df[column] = le.transform(df[column])
            
        return df