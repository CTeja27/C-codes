# Filename: Lab4p1.py
# Author: Chasham Teja
# Course: ITSC203
"""Details: A python program that Enumerate the entire folder in such a way that it is easy to see the folder structure.
 The table below is just an example. You can present the data as a table or in another layout format that is easy to read.

#Resources:“Hashlib - Secure Hashes and Message Digests.” Python Documentation, docs.python.org/3/library/hashlib.html. Accessed 25 Oct. 2023.
“Shutil - High-Level File Operations.” Python Documentation, docs.python.org/3/library/shutil.html. Accessed 25 Oct. 2023.
"""


#!/usr/bin/env python3


import os
import shutil
import hashlib
from prettytable import PrettyTable

# Define source and target directories
source_dir = "folder03a"
target_dir = "Lab4_FileExt"

# Function to create a unique fingerprint for a file
def generate_file_hash(file_path, hash_algorithm):
    hasher = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Ensure the target directory exists, or create it
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

# Create a table for organizing file info
table = PrettyTable()
table.field_names = ["Directory", "Filename", "Hash(SHA256)", "Extensions"]

previous_directory = None


for root, dirs, files in os.walk(source_dir):
    for file in files:
        file_path = os.path.join(root, file)

        sha256_hash = generate_file_hash(file_path, "sha256")
        _, extension = os.path.splitext(file)

        # Organize and display file information in the table
        if previous_directory and previous_directory != root:
            table.add_row(["", "", "", ""])

        # If it's the first file in the directory, display the directory name
        if previous_directory != root:
            table.add_row([root, file, sha256_hash, extension])
        else:
            table.add_row(["", file, sha256_hash, extension])

        previous_directory = root

        ext_target_dir = os.path.join(target_dir, extension[1:])
        os.makedirs(ext_target_dir, exist_ok=True)

        # Copy the file
        shutil.copy(file_path, os.path.join(ext_target_dir, sha256_hash))

# Set the alignment of the table for better readability
table.align["Directory"] = "l"
table.align["Filename"] = "l"
table.align["Hash(SHA256)"] = "l"
table.align["Extensions"] = "l"

# Print the organized table
print(table)


print("Files copied and renamed successfully.")
