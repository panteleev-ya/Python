import shutil
import os


def make_zip_archive(name, directory):
    shutil.make_archive(name, 'zip', directory)


def rm_rf_dir(directory):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), directory)
    shutil.rmtree(path)


def rm(name):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name)
    os.remove(path)
