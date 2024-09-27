from pyspark.sql.functions import col, when, sum as spark_sum
from pyspark.sql import functions as F
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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


def plot_boxplots(df, feature):
    """
    Plots a box plot for a specified column in the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing numeric feature columns.
    feature (str): The column that you want to observe.
    """
    # Set up the figure
    plt.figure(figsize=(8, 6))

    # Boxplot for the feature
    sns.boxplot(y=df[feature])
    plt.title(f'Boxplot of {feature}')

    # Show the plot
    plt.tight_layout()
    plt.show()


def outlier_remover(df, column_name):
    """
    Removes outliers from a specified column in the DataFrame using the IQR method with a custom multiplier for N > 100.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.
    column_name (str): The name of the column from which to remove outliers.

    Returns:
    pandas.DataFrame: DataFrame with outliers removed.
    """
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    
    # Calculate IQR
    IQR = Q3 - Q1
    
    # Get the number of records (N)
    N = len(df)
    
    # Apply the formula for N > 100
    multiplier = np.sqrt(np.log(N) - 0.5)
    
    # Define the lower and upper bounds for outliers
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    # Filter the DataFrame to exclude outliers
    filtered_df = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]
    
    return filtered_df