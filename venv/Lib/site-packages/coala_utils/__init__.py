from os.path import join, dirname


VERSION_FILE = join(dirname(__file__), "VERSION")


def get_version():
    with open(VERSION_FILE, 'r') as ver:
        return ver.readline().strip()


VERSION = get_version()
