from pyunpack import Archive
import patoolib
import os
from os.path import splitext, basename, expanduser, exists, dirname
import shutil
from rarfile import RarFile


def extract(link):  # запись содержимого архива во временную папку
    temp = os.path.join(expanduser('~/.current/'), splitext(basename(link))[0])
    if exists(temp):
        shutil.rmtree(temp)
    os.makedirs(temp)
    # temp2 = 'files'
    Archive(link).extractall(temp)
    # rarfile.RarFile(link).extractall(temp)
    # patoolib.extract_archive(link, temp)
    return os.path.abspath(temp)

def all_pages(link):  # список всех страниц во временной директории
    pages = []
    for root, dirs, files in os.walk(link):
        pages.extend([os.path.join(root, fname) for fname in sorted(files)])
    return pages
