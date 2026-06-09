import pandas as pd
import numpy as np

instructions = {
    "column_name": "method"
}

def handle_missing(df, instructions, fill_value=None):
  """
    Cleans missing values in a specified column of a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.
    column_name (str): The column to clean.
    method (str): How to fill missing values. Options: "mean", "median", "mode", "constant", "drop".
    fill_value: Value to use if method="constant".

    Returns:
    pd.DataFrame: A new DataFrame with the column cleaned.
    """
  for column_name, method in instructions.items():
    if method=="mean":
      df[column_name] = df[column_name].fillna(df[column_name].mean())
    elif method=="median":
      df[column_name] = df[column_name].fillna(df[column_name].median())
    elif method=="mode":
      df[column_name] = df[column_name].fillna(df[column_name].mode()[0])
    elif method=="constant":
      if fill_value is None:
        raise ValueError ("You must provide fill_value when using method ='constant'")
      df[column_name] = df[column_name].fillna(fill_value)
    elif method=="drop":
      df = df.dropna(subset=[column_name])
    else:
      raise ValueError("Choose from the method: mode, mean, median, constant, drop.")

  return df


def remove_duplicates(df):
    """
    Removes duplicates in any given dataframe.

    Parameters:
    df (pd.DataFrame): The Dataframe to remove duplicates.

    Returns:
    pd.DataFrame: A new DataFrame with the duplicates removed.
    """
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    removed = before - after
    print(f"Removed {removed} duplicate rows — {after} rows remaining")
    return df



instructions = {
    "column_name": "dtype"
}
def fix_dtypes(df, instructions):
  """
  Fixes data type issues in specified columns of a DataFrame.
  Cleans numeric-like strings by removing non-digit characters.
    
  Parameters:
  df (pd.DataFrame): The DataFrame whose column dtypes need correction.
  dtype_map (instructions): A dictionary where keys are column names and values are target dtypes.
                      Example: {"age": "int", "bmi": "float", "smoking_status": "category", "price": "currency"}

  Returns:
  pd.DataFrame: A new DataFrame with corrected column dtypes.
  """
  for column_name, dtype in instructions.items():
    if dtype == "numeric":
      df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    elif dtype == "messy_numeric":
      df[column_name] = df[column_name].astype(str)
      df[column_name] = df[column_name].str.replace(r"[^\d.]", "", regex=True)
      df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    elif dtype == "category":
      df[column_name] = df[column_name].astype("category")
    elif dtype == "datetime":
      df[column_name] = pd.to_datetime(df[column_name], errors="coerce")

  return df



def remove_outliers(df, column_name, method="IQR", action="remove"):
  """
  Removes or caps outliers in a specified column using IQR or Zscore method.

  Parameters:
  df          : pd.DataFrame — the dataframe to clean
  column_name : str — the column to check for outliers
  method      : str — 'IQR' (default) or 'Zscores'
  action      : str — 'remove' (default) drops outlier rows
                    'cap' clips values to the boundary

  Returns:
  pd.DataFrame — cleaned dataframe with outliers removed or capped

  Example:
  df = remove_outliers(df, "avg_glucose_level", method="IQR", action="cap")
  df = remove_outliers(df, "bmi", method="Zscores", action="remove")
  """
  before = len(df)
  if method =="IQR":
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    if action == "remove":
      df = df[(df[column_name] >= lower) & (df[column_name] <= upper)]
    elif action == "cap":
      df[column_name] = df[column_name].clip(lower=lower, upper=upper)
    after = len(df)
    if action == "remove":
      print(f"Removed {before-after} outlier rows -- {after} rows remaining")
    elif action == "cap":
      print(f"Capped outliers in '{column_name}' -- all {after} rows retained")

  elif method =="Zscores":
    mean = df[column_name].mean()
    std = df[column_name].std()
    zscores = (df[column_name] - mean) / std
    mask = np.abs(zscores) <=3


    if action == "remove":
        df = df[mask]  
    elif action == "cap":
        lower = mean - 3 * std
        upper = mean + 3 * std
        df[column_name] = df[column_name].clip(lower=lower, upper=upper)

    after = len(df)
    if action == "remove":
        print(f"Removed {before - after} outlier rows -- {after} rows remaining")
    elif action == "cap":
        print(f"Capped outliers in '{column_name}' -- all {after} rows retained")

  return df


def clean_strings(df, columns=None):
  df = df.copy()
  if columns is None:
    columns = df.select_dtypes(include="object").columns.tolist()
  for column in columns:
    df[column] = df[column].str.strip()
    df[column] = df[column].str.lower()

  print(f"Cleaned {len(columns)} string column(s)")
  
  return df

