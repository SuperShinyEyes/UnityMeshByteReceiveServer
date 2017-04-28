import os
from datetime import datetime
PROJECT_NAME = "MeshServer"

def remove_ignored_items_and_dir(file_names):
    # print("Constants.ignored", Constants.ignored)
    ignored = ['.ds_store']
    return [
        i for i in file_names
        if not os.path.isdir(i)  # Remove directories
           and os.path.basename(i).lower() not in ignored  # Ignore unnecessaries
    ]

def get_base_path():
    this_path = os.path.abspath(__file__)
    i= this_path.find(PROJECT_NAME)
    return this_path[:i + len(PROJECT_NAME)]


def get_filenames(target_dir_name):
    basepath = get_base_path()
    target_dir_path = os.path.join(basepath, target_dir_name)
    all_file_names = os.listdir(target_dir_path)
    all_file_names = [os.path.join(target_dir_path, n) for n in all_file_names]
    return remove_ignored_items_and_dir(all_file_names)

def get_target_path(target_path):
    return os.path.join(get_base_path(), target_path)

def get_random_name(extension='.obj'):
    time_format = '%Y-%m-%d-%a-%H:%M:%S:%f'
    filename = datetime.today().strftime(time_format) + extension
    return filename



if __name__ == '__main__':
    print(get_base_path())