import sys
from pathlib import Path as P
import os
from shutil import unpack_archive, ReadError
from normalize import normalize

categories = {
    "IMAGES": "images",
    "VIDEO": "video",
    "DOCUMENTS": "documents",
    "MUSIC": "music",
    "ARCHIVES": "archives",
    "UNDEFINED": "undefined"
}

sorted_dirs = {
    categories["IMAGES"]: ('JPEG', 'PNG', 'JPG', 'SVG'),
    categories["VIDEO"]: ('AVI', 'MP4', 'MOV', 'MKV'),
    categories["DOCUMENTS"]: ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    categories["MUSIC"]: ('MP3', 'OGG', 'WAV', 'AMR'),
    categories["ARCHIVES"]: ('ZIP', 'GZ', 'TAR'),
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
    if category_dir == categories["ARCHIVES"]:
        handle_archive(file)
    else:
        replace_file_to_grouping_dir(file, category_dir)
    parrent_dir = P(file).parent
    if get_is_parrent_dir_empty(parrent_dir):
        os.rmdir(parrent_dir)


def handle_archive(file):
    archive_path = abs_dir_path / categories["ARCHIVES"] / P(file).name
    os.mkdir(archive_path)
    try:
        unpack_archive(file, archive_path)
        os.remove(file)
    except ReadError:
        replace_file_to_grouping_dir(file, categories["UNDEFINED"])
        print(f"File {file} is not archive, so it moves to UNDEFINED directory")


def choose_category_dir(file):
    extension = P(file).suffix[1::]
    for dir_name, exts in sorted_dirs.items():
        if type(exts) == tuple:
            if extension.upper() in exts:
                return dir_name
    return categories["UNDEFINED"]


def replace_file_to_grouping_dir(file, grouping_dir):
    file_name = normalize_file_name(file)
    dest_file = abs_dir_path / grouping_dir / file_name
    os.replace(file, dest_file)


def get_file_data(file):
    filename = P(file).name
    extension = P(file).suffix
    if extension:
        splited_filename = filename.split(".")
        file_name_chunks = splited_filename[0:-1]
        filename = ".".join(file_name_chunks)
    return {"name": filename, "extension": extension}


def normalize_file_name(file):
    file_chunks = get_file_data(file)
    return normalize(file_chunks["name"]) + (file_chunks["extension"] if file_chunks["extension"] else "")


def get_is_parrent_dir_empty(dir):
    return len(os.listdir(dir)) == 0


dir_path = sys.argv[1]
abs_dir_path = P(dir_path).resolve()
# abs_dir_path = os.path.abspath(dir_path)
# absolute_path = P(dir_path, "../../").resolve()

sort_heap(dir_path)
