from pyunpack import Archive
import os
from os.path import splitext, basename, expanduser, exists
import shutil


def extract(link):  # запись содержимого архива во временную директорию
    temp = os.path.join(expanduser('~/.current/'), splitext(basename(link))[0]) 
    if exists(temp):
        shutil.rmtree(temp)
    os.makedirs(temp)
    Archive(link).extractall(temp)
    return os.path.abspath(temp)


def all_pages(link):  # список всех страниц во временной директории
    pages = []
    for root, dirs, files in os.walk(link):
        pages.extend([os.path.join(root, fname) for fname in sorted(files)])
    return pages


def get_book_name(link):  # имя каталога
    return splitext(basename(link))[0]


