# Data Cleaning Toolkit

Data Cleaning Toolkit is a lightweight Python utility package designed to automate common data cleaning tasks. It provides reusable functions for handling missing values, removing duplicates, correcting data types, treating outliers, and standardizing text data. The goal is to reduce repetitive cleaning work and create consistent, reproducible preprocessing workflows for data analysis and machine learning projects.

## Features

- Handle missing values
- Remove duplicate rows
- Fix incorrect data types
- Detect and remove outliers
- Standardize text columns
- Reusable and customizable cleaning workflows


## The Functions

### handle_missing
This function when called upon handles the missing values in the dataaset, with options to either fill or drop it. The parameters it takes are mean, median, mode, dropna, filling with a constant too. you call it by saying df = handle_missing(df, instructions, fill_value=None); instructions = {
    "Age": "median",
    "Salary": "mean",
    "Gender": "mode"
}
The instructions is a dictionary where the colummn name is the key and the method to fill the missing value is the value.

### remove_duplicates
This function removes all the duplicates that can be found in the dataset, which ensures data integrity across all rows. When called on a particular dataset, it states how many rows the of duplicates where removed. To call this function you pass it df = remove_duplicates(df). And it,
 Returns:
    pd.DataFrame
        Dataset with duplicate rows removed.

### fix_dtypes
This function fixes the issue with wrong data type for column names. When columns are saved with different data types it is difficult to work on the data for example when a price column is saved as object because of special characters like currency symbols and commas, when panda loads the data, it assumes they are objects hence the columns saved as objects. But this tends to cause issues when calcultions are need to be made. Also for date columns which should be saved as datetime datatypes too. 
To call this function;
instructions = {
    "Price": "messy_numeric",
    "Order_Date": "datetime"
}

df = fix_dtypes(df, instructions)
Where instructions is a dictionary that stores the column name as the key and the dtype as the value.

### remove_outliers
This function remove outliers or anomaly from a dataset. There are two options to use inorder to know the benchmark to cut off or cap, they are IQR and Zscores. IQR is recommended for skewed datasets and works using quartiles. While, Z-score is recommended for approximately normal distributions and works using standard deviations from the mean.These two are the ones available for now, hopefully more would be added. The options being used could either use the remove action or cap action. The way to call this function; df = remove_outliers(df, column_name, method="IQR", action="remove")

### clean_strings
This functions works specifically on strings. It cleans strings when there is no unformity across the data. This functions helps to make everything uniformed from making sure all values or categories  in a column are same(all in small letters, no spcace in between, etc). To call this function; df = clean_strings(df, columns=None)
What it does, parameters it takes, example of how to call it.

## Usage
To use it you call it this way, as long as you have the file.
from cleaning_utilitis import (handle_missing, remove_outliers, clean_strings, fix_dtypes, remove_duplicates)

## Requirements
- pandas
- numpy