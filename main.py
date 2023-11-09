import sys
from pathlib import Path as P
import os
from normalize import normalize

sorted_dirs = {
    "зображення": ('JPEG', 'PNG', 'JPG', 'SVG'),
    "відео файли": ('AVI', 'MP4', 'MOV', 'MKV'),
    "документи": ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    "музика": ('MP3', 'OGG', 'WAV', 'AMR'),
    "архіви": ('ZIP', 'GZ', 'TAR'),
    "невідомі": ("*"),
}


def sort_heap(path):
    path_instance = P(path)
    for item in path_instance.iterdir():
        if P(item).is_dir():
            sort_heap(item)
        else:
            handle_file(item)


def handle_file(file):
    category_dir = choose_category_dir(file)
    if category_dir not in os.listdir(dir_path):
        path = abs_dir_path / category_dir
        os.mkdir(path)
    file_name = create_file_name(file)
    dest_file = abs_dir_path / category_dir / file_name
    os.replace(file, dest_file)
    parrent_dir = P(file).parent
    if get_is_parrent_dir_empty(parrent_dir):
        os.rmdir(parrent_dir)


def choose_category_dir(file):
    extension = P(file).suffix[1::]
    for dir_name, exts in sorted_dirs.items():
        if type(exts) == tuple:
            if extension.upper() in exts:
                return dir_name
        else:
            return dir_name


def create_file_name(file):
    extension = P(file).suffix
    file_name_chunks = P(file).name.split(".")[0:-1]
    file_name = ".".join(file_name_chunks)
    normalized_file_name = normalize(file_name)
    full_file_name = normalized_file_name + extension
    return full_file_name


def get_is_parrent_dir_empty(dir):
    return len(os.listdir(dir)) == 0


dir_path = sys.argv[1]
abs_dir_path = P(dir_path).resolve()
# abs_dir_path = os.path.abspath(dir_path)
# absolute_path = P(dir_path, "../../").resolve()

sort_heap(dir_path)
