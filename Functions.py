from win32com.shell import shell, shellcon
import hashlib
import os
from os import listdir
from os.path import *
from File import File_Info
import ctypes


PATH = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0) + "\\PiPi"
MB = 1000000


def get_all_files():
    """
    Creates the special directory of the program if it wasn't already created
    and returns list of File_info objects of all files in folder
    """
    files_object_list = []
    check_folder()
    all_files = find_files()
    for file_object in all_files:
        file_name = file_object[0]  # Only file name
        file_path = file_object[1]  # Its full path
        file_folder = file_path[0:-len(file_name)-1]  # Only the directory it is in
        final_object = get_file_object(file_folder, file_name)
        files_object_list.append(final_object)
    return files_object_list


def find_files():
    """
    Returns a list of all of the files in PiPi directory
    The list is made of (name, path) for every file found
    """
    files_list = []
    for root, dirs, files in os.walk(PATH):
        for basename in files:
            file_path = os.path.join(root, basename)
            if not is_hidden(file_path):
                files_list.append([basename, file_path])
    return files_list


def decrypt_file(file_object):
    """
    Receives a base64 file to_string and returns a new file object
    """
    file_info = file_object.decode("base64")
    file_name, file_description, file_size, file_num_of_parts, file_hash = file_info.split(';')
    return File_Info(file_name, file_description, file_size, file_num_of_parts, file_hash)


def check_if_new_file(files_list):
    """
    Checks if a new file was added to the sharing folder
    """
    new_files_list = get_all_files()
    return new_files_list == files_list


def get_file_object(file_path, name):
    """
    Returns an object of type File_Info for the file 'name' in file_path
    """
    _hash = sha1_of_file(file_path + "\\" + name)
    file_size = os.path.getsize(file_path)
    description_path = file_path + "\\" + _hash + ".txt"
    if os.path.isfile(description_path):
        description = open(description_path, 'r').read()
    else:
        create_description(description_path)
        description = open(description_path, 'r').read()
    if file_size % MB == 0:
        num_of_parts = file_size / MB
    else:
        num_of_parts = file_size / MB + 1
    final_object = File_Info(name, description, file_size, num_of_parts, _hash)
    return final_object


def sha1_of_file(file_path):
    """
    Returns sha1 of file
    """
    with open(file_path, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()


def check_folder():
    """ Create folder if it doesn't exist """
    if not os.path.exists(PATH):
        os.makedirs(PATH)


def create_description(description_path):
    """
    Creates a description hidden txt file for a specific file, txt file name is sha1 of file
    """
    description = open(description_path, 'w')
    description.write("No Description")
    description.close()
    os.popen('attrib +h ' + description_path)


def is_hidden(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    return name.startswith('.') or has_hidden_attribute(filepath)


def has_hidden_attribute(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result