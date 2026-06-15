# Data Cleaning Toolkit
# Version: 1.0.0
# Author: Ugorji Maxwell

import pandas as pd
import numpy as np

instructions = {
    "column": "method"
}

def handle_missing(df, instructions, fill_value=None):
  """
    Cleans missing values in a specified column of a DataFrame.

  Parameters:
  df           : pd.DataFrame, the dataframe to clean
  instructions : dict — keys are column names, values are methods(mean, median, mode, constant, drop). Example: {"bmi": "median", "age": "mean"}
  fill_value   : value to use when method is "constant"

    Returns:
    pd.DataFrame: A new DataFrame with the column cleaned.
  """
  if not isinstance(instructions, dict):
    raise TypeError("instructions must be a dictionary — example: {'bmi': 'median'}")
  for column in instructions:
    if column not in df.columns:
        raise ValueError(f"Column '{column}'not found in dataframe. Check your column names.")
  total_missing_before = df.isnull().sum().sum()
  for column, method in instructions.items():
    if method=="mean":
      df[column] = df[column].fillna(df[column].mean())
    elif method=="median":
      df[column] = df[column].fillna(df[column].median())
    elif method=="mode":
      df[column] = df[column].fillna(df[column].mode()[0])
    elif method=="constant":
      if fill_value is None:
        raise ValueError ("You must provide fill_value when using method ='constant'")
      df[column] = df[column].fillna(fill_value)
    elif method=="drop":
      df = df.dropna(subset=[column])
      print(f" Number of rows remaining after dropping missing values in '{column}': {df.shape[0]} rows")
    else:
      raise ValueError("Choose from the method: mode, mean, median, constant, drop.")
  total_missing_after = df.isnull().sum().sum()
  print(f"Missing values handled. Total missing values before: {total_missing_before} | after: {total_missing_after}")

  return df 


def remove_duplicates(df):
  """
  Removes duplicates in any given dataframe.
  Parameters:
  df :(pd.DataFrame) - the Dataframe to remove duplicates from
  Returns:
  pd.DataFrame: A new DataFrame with the duplicates removed.
  """
  df = df.copy()
  before = len(df)
  df = df.drop_duplicates()
  after = len(df)
  removed = before - after
  print(f"Removed {removed} duplicate rows — {after} rows remaining")
  return df



instructions = {
    "column": "dtype"
}

def fix_dtypes(df, instructions):
  """
  Fixes data type issues in specified columns of a DataFrame &
  Cleans numeric-like strings by removing non-digit characters.
    
  Parameters:
  df : pd.DataFrame, the DataFrame whose column dtypes need correction.
  Instructions: A dictionary where keys are column names and values are target dtypes.
                Example: {"age": "numeric", "signup_date": "datetime", "price": "messy_numeric"}

  Returns:
  pd.DataFrame: A new DataFrame with corrected column dtypes.
  """
  if not isinstance(instructions, dict):
    raise TypeError("Instructions must be a dictionary — example: {'age': 'numeric'}")
  for column in instructions:
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataframe. Check your column names.")
  for column, dtype in instructions.items():
    if dtype == "numeric":
      df[column] = pd.to_numeric(df[column], errors="coerce")
    elif dtype == "messy_numeric":
      df[column] = df[column].astype(str)
      df[column] = df[column].str.replace(r"[^\d.]", "", regex=True)
      df[column] = pd.to_numeric(df[column], errors="coerce")
    elif dtype == "category":
      df[column] = df[column].astype("category")
    elif dtype == "datetime":
      df[column] = pd.to_datetime(df[column], errors="coerce")

  new_nulls = df[list(instructions.keys())].isnull().sum()
  new_nulls = new_nulls[new_nulls > 0]
  if not new_nulls.empty:
    print(f"Warning: After converting dtypes, the following columns have new null values:\n{new_nulls}")
  else:
    print("Dtypes fixed successfully with no new null values introduced.")

  return df



def remove_outliers(df, column, method="IQR", action="remove"):
  """
  Removes or caps outliers in a specified column using IQR or Zscore method.

  Parameters:
  df          : pd.DataFrame — the dataframe to clean
  column      : str — the column to check for outliers
  method      : str — 'IQR' (default) or 'Zscores'
  action      : str — 'remove' (default) drops outlier rows
                    'cap' clips values to the boundary

  Returns:
  pd.DataFrame — cleaned dataframe with outliers removed or capped

  Example:
  df = remove_outliers(df, "avg_glucose_level", method="IQR", action="cap")
  df = remove_outliers(df, "bmi", method="Zscores", action="remove")
  """
  if column not in df.columns:
    raise ValueError(f"Column '{column}' not found in dataframe. Check your column names.")
  if method not in ["IQR", "Zscores"]:
    raise ValueError("Method must be 'IQR' or 'Zscores'.")
  if action not in ["remove", "cap"]:
    raise ValueError("Action must be 'remove' or 'cap'.")
  if not pd.api.types.is_numeric_dtype(df[column]):
    raise TypeError(f"Column '{column}' must be numeric for outlier removal")
  before = len(df)
  if method =="IQR":
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    if action == "remove":
      df = df[(df[column] >= lower) & (df[column] <= upper)]
    elif action == "cap":
      df[column] = df[column].clip(lower=lower, upper=upper)
    after = len(df)
    if action == "remove":
      print(f"Removed {before-after} outlier rows -- {after} rows remaining")
    elif action == "cap":
      print(f"Capped outliers in '{column}' -- all {after} rows retained")

  elif method =="Zscores":
    mean = df[column].mean()
    std = df[column].std()
    zscores = (df[column] - mean) / std
    mask = np.abs(zscores) <=3


    if action == "remove":
        df = df[mask]  
    elif action == "cap":
        lower = mean - 3 * std
        upper = mean + 3 * std
        df[column] = df[column].clip(lower=lower, upper=upper)

    after = len(df)
    if action == "remove":
        print(f"Removed {before - after} outlier rows -- {after} rows remaining")
    elif action == "cap":
        print(f"Capped outliers in '{column}' -- all {after} rows retained")

  return df


def clean_strings(df, columns=None):
  """
  Cleans string columns by stripping whitespace and converting to lowercase.
  Parameters:
  df : pd.DataFrame - the DataFrame to clean
  columns : list of str (optional) - specific columns to clean. If None, all object-type columns will be cleaned.
  Returns:  
  pd.DataFrame - a new DataFrame with cleaned string columns.
  """
  if columns is not None:
    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in dataframe. Check your column names.")
  if columns is not None and not isinstance(columns, list):
    raise TypeError("columns must be a list — example: ['gender', 'smoking_status']")
  df = df.copy()
  if columns is None:
    columns = df.select_dtypes(include="object").columns.tolist()
  for column in columns:
    df[column] = df[column].str.strip()
    df[column] = df[column].str.lower()

  print(f"Cleaned {len(columns)} string column(s)")
  
  return df

