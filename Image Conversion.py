from PIL import Image
from pillow_heif import register_heif_opener
import os
import re
import time

def convert_dir(current_dir = None, recurse = False, success = [], warning = [], error = []):
    """Opens the current directory and converts all HEIC files into JPG files.
       Capable of recursing through sub-directories."""
    files = os.listdir(current_dir) #generate list of files in directory
    #print(files)
    heic = [] #initialize a list to store heic files
    register_heif_opener() #allow opening heic files

    for i in files: #iterate through files to find heic files
        #print("iterating: " + i)
        if re.match('.+\.heic$', i, re.IGNORECASE):
            heic.append(i)
        elif os.path.isdir(current_dir + "\\" + i) and recurse == True:
            success, warning, error = convert_dir(current_dir + "\\" + i, True, success, warning, error) #recursively opens and converts files

    for f in heic:
        # print("Converting: " + f)
        img = Image.open(current_dir + "\\" + f)
        pre, ext = os.path.splitext(f)
        new_name = pre + ".JPG"
        if new_name in files:
            print("WARNING: " + new_name + " already exists. Aborting.")
            warning.append(current_dir + "\\" + new_name)
        else:
            try:
                img = img.save(current_dir + "\\" + new_name, 'jpeg')
                print("Converted: " + f)
                success.append(current_dir + "\\" + new_name)
            except OSError:
                print("ERROR: " + pre + " not converted! (Image contains transparent pixels?)")
                error.append(current_dir + "\\" + pre)

    return success, warning, error            

def convert_file(path = None):
    """Converts a single HEIC file into a JPG file"""
    register_heif_opener()
    print("Converting: " + path)
    img = Image.open(path)
    pre, ext = os.path.splitext(path)
    new_name = pre + ".JPG"
    img = img.save(new_name, 'JPEG')

def path_handler():
    """Takes and validates user input for the path."""
    val = input("Please enter path of directory containing .HEIC images. If no path is provided, the current directory will be opened:\n")
    if re.match('^quit$', val, re.IGNORECASE):
        quit()
    elif os.path.isfile(val):
        print("Converting single files is currently disabled due to bugs.")
    elif not (os.path.isdir(val)):
        print("The path you have entered is not valid. Please enter a valid path. Or type 'quit' to quit.")
        val = path_handler()
    return val

def recurse_handler():
    """Takes and validates user input for recursion."""
    recurse = input("Do you want to convert sub-directories? (does not apply when converting a single file) (y/n): ")
    if re.match('^quit$', recurse, re.IGNORECASE):
        quit()
    elif re.match('^y$', recurse, re.IGNORECASE):
        recurse = True
    elif re.match('^n$', recurse, re.IGNORECASE):
        recurse = False
    else:
        print("Please enter 'y' for yes or 'n' for no. Or type 'quit' to quit.")
        recurse = recurse_handler()
    return recurse

def gen_log(success, warning, error, current_dir = None):
    content = "Success: " + str(len(success)) + "\n"
    for each in success:
        content += "  " + each + "\n"
    content += "\nDuplicate Name: " + str(len(warning)) + "\n"
    for each in warning:
        content += "  " + each + "\n"
    content += "\nError: " + str(len(error)) + "\n"
    for each in error:
        content += "  " + each + "\n"
    
    num = int(0)
    files = os.listdir(current_dir)
    for f in files:
        if re.match('^log\.[0-9]+.txt$', f):
            split = f.split('.', 2)
            if int(split[1]) > int(num):
                num = split[1]
    filename = "log." + str(int(num) + 1) + ".txt"
    print(filename)

    if os.path.isfile(current_dir + "\\" + filename):
        print("this is a bug :/")
    else:
        f = open(current_dir + "\\" + filename, 'w')
        f.write(content)
        f.close()
        


def run(path, recurse = True):
    #path = path_handler()
    #recurse =  recurse_handler()

    start = time.time_ns()
    print("")

    if os.path.isdir(path):
        success, warning, error = convert_dir(path, recurse)
        print("\nSuccess: " + str(len(success)))
        print("Duplicate Name: " + str(len(warning)))
        print("Error: " + str(len(error)))
        gen_log(success, warning, error, path)
        success.clear()
        warning.clear()
        error.clear()

    elif os.path.isfile(path):
        convert_file(path)


    end = time.time_ns()
    time_consumed = end - start
    time_consumed_ms = time_consumed / 1000000000
    print(path)
    print("Done! (" + str(time_consumed_ms) + " seconds)\n")

for i in range(10):
    run("C:\\Users\\SelfBuilt\\Desktop\\Test HEIC")

