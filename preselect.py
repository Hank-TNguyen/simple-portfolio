import os
import shutil
from tkinter import Tk, filedialog

# Prompt the user to select the source directory
Tk().withdraw()
source_directory = filedialog.askdirectory(title='Select Source Directory')

# Read the image names from the file
with open('names.txt', 'r') as file:
    image_names = file.read().splitlines()

# Create the destination directory if it doesn't exist
destination_directory = 'images/'
os.makedirs(destination_directory, exist_ok=True)

# Loop through the image names and copy the corresponding images
for image_name in image_names:
    source_file = os.path.join(source_directory, f"{image_name}")
    destination_file = os.path.join(destination_directory, f"{image_name}")
    if os.path.isfile(source_file):
        shutil.copy(source_file, destination_file)
        print(f"Copied {source_file} to {destination_file}")
    else:
        print(f"Image file {source_file} not found")

print("Image copying completed.")
