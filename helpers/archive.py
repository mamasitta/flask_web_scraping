import errno
import os
import zipfile
from datetime import datetime

from flask import send_file


# create archive for downloading with all pages from link (name of archive - name of website, name of file - url)
def create_archive(pages, link):
    # processing data for dirname
    dir = link[8:].replace('/', '')
    dir = dir.split('.')
    date = datetime.now()
    str_date = date.strftime("%m%d%Y%H%M%S")
    dirname = dir[0]
    # writing files in directory
    for page in pages:
        name = page.name.replace("/", "")
        os.makedirs(os.path.dirname('{}{}/{}.txt'.format(dirname, str_date, name)), exist_ok=True)
        with open('{}{}/{}.txt'.format(dirname, str_date, name), "w", encoding="utf-8") as f:
            f.write("{}".format(page.text))
    return '{}{}'.format(dirname, str_date)




