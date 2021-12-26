import os
import re
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def save_image(image, folder):
    return IMAGE_SET.save(image, folder)


def get_path(filename, folder):
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename, folder):
    # """
    # Given a format-less filename, try to find the file by appending each of the allowed formats to the given
    # filename and check if the file exists
    # :param filename: format less filename
    # :param folder: the relative folder in which to search
    # :return: the path of the image if exists, otherwise None
    # """
    for _format in IMAGES:  # look for existing avatar and delete it
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file):
    """
    Make our filename related functions generic, able to deal with FileStorage object as well as filename str.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file):
    """
    Check if a filename is secure according to our definition
    - starts with a-z A-Z 0-9 at least one time
    - only contains a-z A-Z 0-9 and _().-
    - followed by a dot (.) and a allowed_format at the end
    """
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)
    # format IMAGES into regex, eg: ('jpeg','png') --> 'jpeg|png'
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file):
    """
    Return file's basename, for example
    get_basename('some/folder/image.jpg') returns 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file):
    """
    Return file's extension, for example
    get_extension('image.jpg') returns '.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
