from pyspark.sql.functions import col, when, sum as spark_sum
from pyspark.sql import functions as F

def print_dataset_shape(description, sdf):
    """
    Function to print the shape of a Spark DataFrame.

    Parameters:
    description (str): Description of the step in preprocessing.
    sdf (DataFrame): The Spark DataFrame to describe.

    Returns:
    None
    """
    num_rows = sdf.count()
    num_cols = len(sdf.columns)
    print(f"{description} - Shape: ({num_rows} rows, {num_cols} columns)")



def check_missing_values(sdf):
    """
    This function counts the records with missing values.

    Input parameters:  
    sdf : pyspark.sql.DataFrame; The Spark DataFrame in which to check for missing values.

    Output: 
    missing_values_dict: dict; 
    A dictionary containing the count of missing values
    """
    # An empty dictionary that store the count of missing values for each column by month.
    missing_values_dict = {}

    # Count the null values for each column and only keep those with missing values
    missing_value_count = {col_name: count for col_name, count in sdf.select(
        [spark_sum(col(c).isNull().cast("int")).alias(c) for c in sdf.columns]
        ).collect()[0].asDict().items() if count > 0}

    # Print the missing values
    if missing_value_count:
        print(f"Missing values:")
        for col_name, count in missing_value_count.items():
            print(f" - {col_name}: {count} missing values")
    
    return missing_values_dict


