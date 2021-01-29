import errno
import os
import zipfile

from flask import send_file


def create_archive(pages, link):
    dir = link[8:].replace('/', '')
    dir = dir.split('.')
    dirname = dir[0]
    for page in pages:
        name = page.name.replace("/", "")
        os.makedirs(os.path.dirname('{}/{}.txt'.format(dirname, name)), exist_ok=True)
        with open('{}/{}.txt'.format(dirname, name), "w") as f:
            f.write("{}".format(page.text))
    return '{}'.format(dirname)


# def zip_and_download_archive(archive):

    # os.remove('planeks.zip')


