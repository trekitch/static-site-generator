import os
import shutil


def copy_files(src, dest):

    os.mkdir(dest)

    entries = os.listdir(src)

    # Loop through each entry
    for entry in entries:
        # Create full paths
        source_path = os.path.join(src, entry)
        dest_path = os.path.join(dest, entry)
        
        # Check if it's a file or directory
        if os.path.isfile(source_path):
            # If it's a file, copy it
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
        else:
            # If it's a directory, recursively copy it
            # TODO: Implement recursive call here
            copy_files(source_path, dest_path)