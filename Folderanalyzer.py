# Filename: m3p2.py
# Author: Chasham Teja
# Course: ITSC203
#Details: Write a Python program named m3p2.py that asks the user for a folder to analyze

"""Resources:
“Python Datetime.” Python Dates, www.w3schools.com/python/python_datetime.asp. Accessed 20 Oct. 2023.
“Python - List Files in a Directory.” GeeksforGeeks, GeeksforGeeks, 10 Oct. 2022, www.geeksforgeeks.org/python-list-files-in-a-directory/. """

#!/usr/bin/env python3
import os
from prettytable import PrettyTable
import datetime

# Function to display the folder structure
def print_folder_structure_table(folder_path):
    # Create a table to display the folder structure
    table = PrettyTable()
    table.field_names = ["Folder", "Items"]

    for root, dirs, files in os.walk(folder_path):
        folder_name = os.path.basename(root)
        items = " | ".join(dirs + files)
        table.add_row([folder_name, items])

    print("Folder Structure:")
    print(table)

# Function to check and display files meeting or not meeting criteria
def cdfiles(folder_path, start_date, end_date):
    # Lists to store files that meet and don't meet the criteria
    files_meet_criteria = []
    files_dont_meet_criteria = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if start_date <= modified_date <= end_date:
                files_meet_criteria.append((file_path, modified_date))
            else:
                files_dont_meet_criteria.append((file_path, modified_date))

    # Display files that meet the criteria
    print("\nFiles that meet your criteria:")
    for file_path, modified_date in files_meet_criteria:
        print(f"File: {os.path.relpath(file_path, folder_path)}")
        print(f"Modified Date: {modified_date}")

    # Display files that don't meet the criteria
    print("\nFiles that don't meet your criteria:")
    for file_path, modified_date in files_dont_meet_criteria:
        print(f"File: {os.path.relpath(file_path, folder_path)}\nDate: {modified_date}")

# Main function
def main():
    # Get the folder path from the user
    folder_path = input("Enter the folder to analyze: ")

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    # Display the folder structure
    print_folder_structure_table(folder_path)

    # Get and validate the date range from the user
    print("\nEnter a date range (YYYY/MM/DD - YYYY/MM/DD): ")
    date_range = input()
    date_range_parts = date_range.split(" - ")

    if len(date_range_parts) != 2:
        print("Invalid date range format. Please use YYYY/MM/DD - YYYY/MM/DD.")
        return

    try:
        start_date = datetime.datetime.strptime(date_range_parts[0], "%Y/%m/%d")
        end_date = datetime.datetime.strptime(date_range_parts[1], "%Y/%m/%d")
    except ValueError:
        print("Invalid date format. Please use YYYY/MM/DD - YYYY/MM/DD.")
        return

    # Check and display files based on the date range
    cdfiles(folder_path, start_date, end_date)

if __name__ == "__main__":
    main()
