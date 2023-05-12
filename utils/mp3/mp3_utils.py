import os


def print_mp3_files(path, is_recursive):
    mp3_files = scan_mp3_files(path, is_recursive)
    count = _count_mp3_files(mp3_files)
    print('%d mp3 file%s has been found:\n' % (count, 's' if count != 1 else ''))
    _print_mp3_files(mp3_files)


def _print_mp3_files(mp3_files, append_first=None):
    mp3s = []
    index = 0
    length = len(mp3_files)
    for file in mp3_files:
        is_last = index == length - 1
        if type(file) == dict:
            for key in file:
                if append_first is not None:
                    print(append_first + ('├── ' if not is_last else '└── ') + os.path.basename(key))
                    _print_mp3_files(file[key], append_first + ('│   ' if not is_last else '    '))
                else:
                    print(os.path.basename(key))
                    _print_mp3_files(file[key], '')
                index += 1
        else:
            mp3s.append(file)
    for mp3 in mp3s:
        if append_first is not None:
            is_last = index == length - 1
            print(append_first + ('├── ' if not is_last else '└── ') + os.path.basename(mp3))
        else:
            print(os.path.basename(mp3))
        index += 1


def scan_mp3_files(path, is_recursive):
    """
    Return a list of every mp3 file found in the current path and sub-paths if is_recursive is set as True.

    If it found mp3 files inside a folder it will put as an element in the list a dict which hold the folder name as
    the key and a list of mp3 files.

    i.e. ['1.mp3', '2.mp3', {'folder': ['3.mp3', '4.mp3']}].

    :param path: current path where it will start the search
    :param is_recursive: if it will search into sub-paths
    :return: list of mp3 files and folders which contains them
    """
    response = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            if is_recursive:
                dir_response = scan_mp3_files(os.path.abspath(file_path), is_recursive)
                if len(dir_response) > 0:
                    response.append({os.path.abspath(file_path): dir_response})
        else:
            if file.lower().endswith('.mp3'):
                response.append(os.path.abspath(file_path))
    return response


def _count_mp3_files(mp3_files):
    count = 0
    for file in mp3_files:
        if type(file) == dict:
            for key in file:
                count += _count_mp3_files(file[key])
        else:
            count += 1
    return count
