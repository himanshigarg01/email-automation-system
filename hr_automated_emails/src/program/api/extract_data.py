import os
import sys
import time
import smtplib
import pandas as pd

# Function to read the receiver's email addresses and names from a CSV file
def get_receivers(filepath):
    """
    This function reads a CSV file containing email addresses and names of receivers.
    The email addresses are expected to be in the second column and names in the third column.

    Args:
    filepath (str): The path to the CSV file.

    Returns:
    list: A list of email addresses.
    list: A list of corresponding names.
    """
    try:
        receivers_data = pd.read_csv(filepath)  # Read the CSV file into a DataFrame
        receivers = []  # Initialize an empty list to store email addresses
        names = []      # Initialize an empty list to store names

        # Loop through the DataFrame to fetch the email addresses and names
        for i in range(0, len(receivers_data)):
            receivers.append(receivers_data.iloc[i, 1])  # Extract email address from the second column
            # Replace empty or "-" names with "Team"
            name = receivers_data.iloc[i, 2]   # Extract name from the third column
            names.append("Team" if pd.isna(name) or name == "-" else name)    
        
        return receivers, names  # Return the list of email addresses and names

    except Exception as e:
        # Print error message with line number
        print(f"Error in get_receivers function: {e} at line {sys.exc_info()[-1].tb_lineno}")
        sys.exit(1)  # Exit the script if an error occurs