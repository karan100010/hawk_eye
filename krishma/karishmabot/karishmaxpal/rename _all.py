#write a function that renames all files in a directory and subdirectories where if argument one is in the file it gets repalced by argument 2
import os
import shutil
import sys

def rename_files(path, old, new):
    for root, dirs, files in os.walk(path):
        for file in files:
            if old in file:
                os.rename(os.path.join(root, file), os.path.join(root, file.replace(old, new))) 
