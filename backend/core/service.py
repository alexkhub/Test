import os


def delete_old_file(path_file):
    if os.path.exists(path_file):
        os.remove(path_file)
