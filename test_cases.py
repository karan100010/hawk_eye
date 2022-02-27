#write a test case testing get_all_data function
import os


#given a path to a folder get all the files and folders
#then using arguments substring and replace_with
#if the file or path contains substring replace it with replace_with
#if the file or path is a folder recursively call this function
#if the file or path is a file then rename it
#if the file or path is a folder then rename it
#if the file or path is a file then save it in the same folder
#if the file or path is a folder then save it in the same folder
#if the file or path is a file then save it in the same folder
def replace(path,substring,replace_with):
    if os.path.isfile(path):
        if substring in path:
            os.rename(path,path.replace(substring,replace_with))
        else:
            os.rename(path,path.replace(os.path.basename(path),replace_with))
    elif os.path.isdir(path):
        for file in os.listdir(path):
            replace(os.path.join(path,file),substring,replace_with)
    else:
        print("file or folder not found")